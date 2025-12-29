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

USER_AGENT = "cncf-opportunities-updater/1.0"
MAX_LFX_PAGES = int(os.environ.get("LFX_MAX_PAGES", "10"))


def load_sources():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing config file: {CONFIG_PATH}")
    return json.loads(CONFIG_PATH.read_text())


def fetch_yaml(url):
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=30) as response:
        return yaml.safe_load(response)


def fetch_json(url):
    req = Request(url, headers={"User-Agent": USER_AGENT})
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


def main():
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

    print(f"Updated {FIRST_TIME_PATH}")
    print(f"Updated {MENTORSHIPS_PATH}")
    print(f"Updated {INTERNSHIPS_PATH}")


if __name__ == "__main__":
    main()
