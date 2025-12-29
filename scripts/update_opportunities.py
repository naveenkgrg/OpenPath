#!/usr/bin/env python3
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
DATA_DIR = ROOT / "data"

MENTORSHIPS_PATH = DATA_DIR / "mentorships.md"
INTERNSHIPS_PATH = DATA_DIR / "internships.md"
FIRST_TIME_PATH = DATA_DIR / "first_time_issues.md"
GOOD_FIRST_ISSUES_DIR = DATA_DIR / "good_first_issues"

USER_AGENT = "cncf-opportunities-updater/1.0"
MAX_LFX_PAGES = int(os.environ.get("LFX_MAX_PAGES", "10"))
MAX_GOOD_FIRST_ISSUES = int(os.environ.get("GOOD_FIRST_MAX", "30"))

SKILL_SEARCHES = [
    {
        "name": "Python",
        "filename": "python_based.md",
        "query": 'label:"good first issue" state:open -is:pr (python OR django OR flask) in:title,body',
    },
    {
        "name": "PHP",
        "filename": "php_based.md",
        "query": 'label:"good first issue" state:open -is:pr (php OR laravel OR symfony) in:title,body',
    },
    {
        "name": "HTML",
        "filename": "html_based.md",
        "query": 'label:"good first issue" state:open -is:pr (html OR css OR frontend) in:title,body',
    },
    {
        "name": "CNCF Projects",
        "filename": "cncf_projects.md",
        "query": 'label:"good first issue" state:open -is:pr org:cncf',
    },
    {
        "name": "Kubernetes",
        "filename": "kubernetes_based.md",
        "query": 'label:"good first issue" state:open -is:pr (kubernetes OR k8s) in:title,body',
    },
    {
        "name": "Security",
        "filename": "security_based.md",
        "query": 'label:"good first issue" state:open -is:pr (security OR vulnerability OR secure) in:title,body',
    },
    {
        "name": "Networking",
        "filename": "networking_based.md",
        "query": 'label:"good first issue" state:open -is:pr (network OR networking OR dns OR tcp OR udp) in:title,body',
    },
    {
        "name": "Git",
        "filename": "git_based.md",
        "query": 'label:"good first issue" state:open -is:pr (git OR github) in:title,body',
    },
    {
        "name": "Shell Scripting",
        "filename": "shell_scripting_based.md",
        "query": 'label:"good first issue" state:open -is:pr (bash OR "shell script" OR shell) in:title,body',
    },
    {
        "name": "Salt",
        "filename": "salt_based.md",
        "query": 'label:"good first issue" state:open -is:pr (saltstack OR "salt") in:title,body',
    },
    {
        "name": "Chef",
        "filename": "chef_based.md",
        "query": 'label:"good first issue" state:open -is:pr (chef OR "chef infra") in:title,body',
    },
    {
        "name": "Monitoring",
        "filename": "monitoring_based.md",
        "query": 'label:"good first issue" state:open -is:pr (monitoring OR observability OR metrics) in:title,body',
    },
    {
        "name": "SRE",
        "filename": "sre_based.md",
        "query": 'label:"good first issue" state:open -is:pr ("sre" OR reliability) in:title,body',
    },
    {
        "name": "DevOps",
        "filename": "devops_based.md",
        "query": 'label:"good first issue" state:open -is:pr (devops OR cicd OR "ci/cd") in:title,body',
    },
]


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
        issues = search_github_issues(skill["query"], MAX_GOOD_FIRST_ISSUES)
        write_good_first_issue_file(skill, issues, timestamp)


def main():
    load_dotenv()
    sources = load_sources()
    landscape_url = sources.get("cncf_landscape_yaml")
    lfx_projects_url = sources.get("lfx_mentorship_projects")
    if not landscape_url or not lfx_projects_url:
        raise KeyError("Missing cncf_landscape_yaml or lfx_mentorship_projects in config/sources.json")
    landscape = fetch_yaml(landscape_url)
    cncf_projects = extract_cncf_projects(landscape)

    first_time_rows = build_first_time_issues(cncf_projects)
    write_first_time(first_time_rows)

    lfx_projects = fetch_lfx_projects(lfx_projects_url)
    mentorship_rows = build_mentorships(lfx_projects, cncf_projects)
    write_mentorships(mentorship_rows)
    write_internships(mentorship_rows)
    write_good_first_issues(SKILL_SEARCHES)

    print(f"Updated {FIRST_TIME_PATH}")
    print(f"Updated {MENTORSHIPS_PATH}")
    print(f"Updated {INTERNSHIPS_PATH}")
    print(f"Updated {GOOD_FIRST_ISSUES_DIR}")


if __name__ == "__main__":
    main()
