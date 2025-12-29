#!/usr/bin/env python3
import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "sources.json"
SKILLS_PATH = ROOT / "config" / "skills.json"
DATA_DIR = ROOT / "data"

MENTORSHIPS_PATH = DATA_DIR / "mentorships.md"
INTERNSHIPS_PATH = DATA_DIR / "internships.md"
FIRST_TIME_PATH = DATA_DIR / "first_time_issues.md"
GOOD_FIRST_ISSUES_DIR = DATA_DIR / "good_first_issues"

USER_AGENT = "cncf-opportunities-updater/1.0"
MAX_LFX_PAGES = int(os.environ.get("LFX_MAX_PAGES", "10"))
MAX_GOOD_FIRST_ISSUES = int(os.environ.get("GOOD_FIRST_MAX", "200"))
GOOD_FIRST_REFRESH_DAYS = int(os.environ.get("GOOD_FIRST_REFRESH_DAYS", "7"))

def load_skills():
    if not SKILLS_PATH.exists():
        raise FileNotFoundError(f"Missing skills file: {SKILLS_PATH}")
    skills = json.loads(SKILLS_PATH.read_text())
    if not isinstance(skills, list):
        raise ValueError("config/skills.json must be a list of skill objects")
    for skill in skills:
        if not isinstance(skill, dict):
            raise ValueError("Each skill must be an object with name, filename, and query")
        for field in ("name", "filename", "query"):
            if field not in skill or not skill[field]:
                raise ValueError(f"Skill missing required field: {field}")
    return skills


def load_dotenv():
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_sources():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing config file: {CONFIG_PATH}")
    return json.loads(CONFIG_PATH.read_text())


def fetch_yaml(url, headers=None):
    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)
    req = Request(url, headers=req_headers)
    with urlopen(req, timeout=30) as response:
        return yaml.safe_load(response)


def fetch_json(url, headers=None):
    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)
    req = Request(url, headers=req_headers)
    with urlopen(req, timeout=30) as response:
        return json.load(response)


def iter_landscape_items(landscape):
    for category in landscape.get("landscape", []):
        for subcategory in category.get("subcategories", []):
            for item in subcategory.get("items", []):
                if isinstance(item, dict):
                    yield item


def normalize_level(item):
    level = item.get("project") or item.get("cncf_relation") or ""
    if not isinstance(level, str):
        return ""
    level = level.strip().lower()
    if level in {"graduated", "incubating", "sandbox"}:
        return level.title()
    return ""


def extract_cncf_projects(landscape):
    projects = []
    for item in iter_landscape_items(landscape):
        level = normalize_level(item)
        if not level:
            continue
        name = item.get("name")
        if not name:
            continue
        projects.append(
            {
                "name": name,
                "level": level,
                "homepage": (item.get("homepage_url") or "").strip(),
                "repo": (item.get("repo_url") or "").strip(),
            }
        )
    return projects


def github_repo_from_url(url):
    if not url:
        return ""
    match = re.search(r"github\.com/([^/]+/[^/#?]+)", url)
    if not match:
        return ""
    repo = match.group(1)
    return repo.replace(".git", "")


def build_first_time_issues(projects):
    rows = []
    labels = [
        ("good first issue", 'is:issue is:open label:"good first issue"', "GitHub label search"),
        ("help wanted", 'is:issue is:open label:"help wanted"', "GitHub label search"),
        ("beginner", 'is:issue is:open label:"beginner"', "GitHub label search"),
        ("easy", 'is:issue is:open label:"easy"', "GitHub label search"),
        ("starter", 'is:issue is:open label:"starter"', "GitHub label search"),
    ]
    for project in sorted(projects, key=lambda p: p["name"].lower()):
        repo = github_repo_from_url(project["repo"])
        if not repo:
            continue
        for label, query, note in labels:
            link = f"https://github.com/{repo}/issues?q={quote(query)}"
            rows.append((project["name"], label, link, note))
    return rows


def fetch_lfx_projects(api_url):
    projects = []
    next_key = None
    seen_keys = set()
    for _ in range(MAX_LFX_PAGES):
        url = api_url
        if next_key:
            url = f"{api_url}?nextPageKey={quote(next_key)}"
        data = fetch_json(url)
        projects.extend(data.get("projects", []))
        next_key = data.get("nextPageKey")
        if not next_key or next_key in seen_keys:
            break
        seen_keys.add(next_key)
    return projects


def github_headers():
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def search_github_issues(query, limit):
    items = []
    page = 1
    per_page = min(100, limit)
    seen = set()
    while len(items) < limit:
        url = (
            "https://api.github.com/search/issues?"
            f"q={quote(query)}&sort=updated&order=desc&per_page={per_page}&page={page}"
        )
        data = fetch_json(url, headers=github_headers())
        results = data.get("items", [])
        if not results:
            break
        for issue in results:
            issue_id = issue.get("id")
            if issue_id in seen:
                continue
            seen.add(issue_id)
            items.append(issue)
            if len(items) >= limit:
                break
        page += 1
    return items


def fetch_repo_stars(repo_full_name, cache):
    if repo_full_name in cache:
        return cache[repo_full_name]
    url = f"https://api.github.com/repos/{repo_full_name}"
    data = fetch_json(url, headers=github_headers())
    stars = data.get("stargazers_count", 0)
    cache[repo_full_name] = stars
    return stars


def repo_full_name_from_issue(issue):
    repo_url = issue.get("repository_url") or ""
    parts = repo_url.rsplit("/", 2)
    if len(parts) != 3:
        return ""
    return f"{parts[1]}/{parts[2]}"


def issue_sort_key(issue, star_cache):
    repo_name = repo_full_name_from_issue(issue)
    stars = fetch_repo_stars(repo_name, star_cache) if repo_name else 0
    return (stars, issue.get("updated_at") or "")


def format_terms(apprentice_needs):
    terms = []
    program_terms = (apprentice_needs or {}).get("programTerms") or {}
    if program_terms.get("spring"):
        terms.append("Spring")
    if program_terms.get("summer"):
        terms.append("Summer")
    if program_terms.get("fall"):
        terms.append("Fall")
    if program_terms.get("ongoing"):
        terms.append("Ongoing")
    if program_terms.get("custom"):
        terms.append(str(program_terms.get("custom")))
    return ", ".join(terms) if terms else "Not specified"


def is_cncf_project(lfx_project, cncf_names, cncf_repos, cncf_homepages):
    name = (lfx_project.get("name") or "").strip()
    repo_link = (lfx_project.get("repoLink") or "").strip()
    website = (lfx_project.get("websiteUrl") or "").strip()
    if name.lower().startswith("cncf"):
        return True
    if name.lower() in cncf_names:
        return True
    repo = github_repo_from_url(repo_link)
    if repo and repo in cncf_repos:
        return True
    if website and website in cncf_homepages:
        return True
    return False


def build_mentorships(lfx_projects, cncf_projects):
    cncf_names = {p["name"].lower() for p in cncf_projects}
    cncf_repos = {github_repo_from_url(p["repo"]) for p in cncf_projects}
    cncf_repos.discard("")
    cncf_homepages = {p["homepage"] for p in cncf_projects if p["homepage"]}

    rows = []
    for project in lfx_projects:
        if not is_cncf_project(project, cncf_names, cncf_repos, cncf_homepages):
            continue
        slug = project.get("slug") or ""
        application = (
            f"https://mentorship.lfx.linuxfoundation.org/#/projects/{slug}"
            if slug
            else "https://mentorship.lfx.linuxfoundation.org/"
        )
        cohort = format_terms(project.get("apprenticeNeeds"))
        accept = project.get("acceptApplications")
        status = "Accepting applications" if accept else "Not accepting applications"
        rows.append(
            (
                "LFX Mentorship",
                project.get("name", "").strip(),
                cohort,
                application,
                status,
            )
        )
    rows.sort(key=lambda r: r[1].lower())
    return rows


def write_mentorships(rows):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# CNCF Mentorships",
        "",
        f"_Last updated: {timestamp}_",
        "_Generated from LFX Mentorship API. Increase pagination with LFX_MAX_PAGES if needed._",
        "",
        "| Program | Org | Cohort | Application | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    MENTORSHIPS_PATH.write_text("\n".join(lines) + "\n")


def write_internships(rows):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# CNCF Internships",
        "",
        f"_Last updated: {timestamp}_",
        "_Generated from LFX Mentorship API. Increase pagination with LFX_MAX_PAGES if needed._",
        "",
        "| Program | Org | Season | Application | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        program, org, cohort, application, status = row
        notes = f"{status}. Mentorship-style program."
        lines.append(f"| {program} | {org} | {cohort} | {application} | {notes} |")
    INTERNSHIPS_PATH.write_text("\n".join(lines) + "\n")


def write_first_time(rows):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# First-Time Issues (CNCF)",
        "",
        f"_Last updated: {timestamp}_",
        "",
        "| Project | Label / Search | Link | Notes |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    FIRST_TIME_PATH.write_text("\n".join(lines) + "\n")


def summarize_issue_body(body, max_len=160):
    if not body:
        return "No summary provided."
    cleaned = " ".join(body.split())
    if len(cleaned) <= max_len:
        return cleaned
    return cleaned[: max_len - 3].rstrip() + "..."


def format_issue_updated_at(updated_at):
    if not updated_at:
        return ""
    if updated_at.endswith("Z"):
        updated_at = updated_at[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(updated_at)
    except ValueError:
        return ""
    return parsed.date().isoformat()


def write_good_first_issue_file(skill, issues, timestamp):
    path = GOOD_FIRST_ISSUES_DIR / skill["filename"]
    lines = [
        f"# Good First Issues: {skill['name']}",
        "",
        f"_Last updated: {timestamp}_",
        "",
        "| Project / Issue (Summary) | Updated | Link |",
        "| --- | --- | --- |",
    ]
    for issue in issues:
        repo = issue.get("repository_url", "").rsplit("/", 2)[-2:]
        project = "/".join(repo) if len(repo) == 2 else "Unknown"
        title = (issue.get("title") or "").strip()
        summary = summarize_issue_body(issue.get("body") or "")
        updated = format_issue_updated_at(issue.get("updated_at") or "")
        link = issue.get("html_url") or ""
        combined = f"{project} - {title} ({summary})"
        lines.append(f"| {combined} | {updated} | {link} |")
    path.write_text("\n".join(lines) + "\n")


def write_good_first_issues(skills):
    GOOD_FIRST_ISSUES_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    for skill in skills:
        print(f"Fetching good first issues for {skill['name']}...")
        issues = search_github_issues(skill["query"], MAX_GOOD_FIRST_ISSUES)
        print(f"  Retrieved {len(issues)} issues. Sorting by repo popularity...")
        star_cache = {}
        issues.sort(key=lambda issue: issue_sort_key(issue, star_cache), reverse=True)
        write_good_first_issue_file(skill, issues, timestamp)
        print(f"  Wrote {skill['filename']}")


def should_refresh_good_first_issues(force_refresh, skills=None):
    if force_refresh:
        return True
    if skills:
        existing_files = [GOOD_FIRST_ISSUES_DIR / skill["filename"] for skill in skills]
    else:
        existing_files = list(GOOD_FIRST_ISSUES_DIR.glob("*.md"))
    if not existing_files:
        return True
    cutoff = datetime.now(timezone.utc).timestamp() - (GOOD_FIRST_REFRESH_DAYS * 86400)
    stale = False
    for path in existing_files:
        if not path.exists():
            return True
        if path.stat().st_mtime < cutoff:
            stale = True
    return stale


def find_skill_by_name(skill_name, skills):
    normalized = skill_name.strip().lower()
    for skill in skills:
        if skill["name"].lower() == normalized:
            return skill
        if skill["filename"].lower() == normalized:
            return skill
    return None


def main():
    parser = argparse.ArgumentParser(description="Update CNCF opportunities data.")
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Force refresh of good first issues even if updated recently.",
    )
    parser.add_argument(
        "--skill",
        help="Refresh good first issues for a specific skill (name or filename).",
    )
    args = parser.parse_args()
    load_dotenv()
    print("Loading sources...")
    sources = load_sources()
    landscape_url = sources.get("cncf_landscape_yaml")
    lfx_projects_url = sources.get("lfx_mentorship_projects")
    if not landscape_url or not lfx_projects_url:
        raise KeyError("Missing cncf_landscape_yaml or lfx_mentorship_projects in config/sources.json")
    print("Fetching CNCF landscape...")
    landscape = fetch_yaml(landscape_url)
    cncf_projects = extract_cncf_projects(landscape)
    print(f"Found {len(cncf_projects)} CNCF projects.")

    print("Building CNCF first-time issues list...")
    first_time_rows = build_first_time_issues(cncf_projects)
    write_first_time(first_time_rows)

    print("Fetching LFX mentorship projects...")
    lfx_projects = fetch_lfx_projects(lfx_projects_url)
    print(f"Found {len(lfx_projects)} LFX projects.")
    mentorship_rows = build_mentorships(lfx_projects, cncf_projects)
    write_mentorships(mentorship_rows)
    write_internships(mentorship_rows)
    skills = load_skills()
    selected_skills = skills
    if args.skill:
        matched = find_skill_by_name(args.skill, skills)
        if not matched:
            print(f"Skill not found: {args.skill}")
            print("Available skills: " + ", ".join(skill["name"] for skill in skills))
            return
        selected_skills = [matched]

    if should_refresh_good_first_issues(args.refresh, selected_skills):
        if args.skill:
            print(f"Writing good first issues for {selected_skills[0]['name']}...")
        else:
            print("Writing skill-based good first issue lists...")
        write_good_first_issues(selected_skills)
    else:
        if args.skill:
            print("Skipping good first issues refresh (recently updated). Use --refresh to override.")
        else:
            print("Skipping good first issues refresh (recently updated). Use --refresh to override.")

    print(f"Updated {FIRST_TIME_PATH}")
    print(f"Updated {MENTORSHIPS_PATH}")
    print(f"Updated {INTERNSHIPS_PATH}")
    print(f"Updated {GOOD_FIRST_ISSUES_DIR}")


if __name__ == "__main__":
    main()
