#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_PATH = DATA_DIR / "internships" / "internship_resources.md"

USER_AGENT = "cncf-opportunities-updater/1.0"
DEFAULT_MAX_RESULTS = int(os.environ.get("INTERNSHIP_MAX", "100"))
DEFAULT_MIN_STARS = int(os.environ.get("INTERNSHIP_MIN_STARS", "100"))
DEFAULT_MIN_WATCHERS = int(os.environ.get("INTERNSHIP_MIN_WATCHERS", "100"))

CACHE_DIR = ROOT / ".cache"
CACHE_PATH = CACHE_DIR / "internship_search.json"
CACHE_DAYS = int(os.environ.get("INTERNSHIP_CACHE_DAYS", "7"))

# Two low-cost searches: a keyword-heavy query plus a topic-based query.
SEARCH_QUERIES = [
    (
        '(internship OR internships OR "summer job" OR "new grad") '
        'in:name,description,readme'
    ),
    (
        '("student program" OR "student jobs" OR "university positions" OR hacktoberfest) '
        'in:name,description,readme'
    ),
    "topic:internship",
]


def load_dotenv():
    # Lightweight .env loader to avoid extra dependencies.
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


def fetch_json(url, headers=None):
    # Shared JSON fetcher with GitHub-friendly headers and timeout.
    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)
    req = Request(url, headers=req_headers)
    try:
        with urlopen(req, timeout=30) as response:
            return json.load(response)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", "ignore")
        return {"_error": True, "status": exc.code, "message": body or exc.reason}


def github_headers():
    # Use a token if available to avoid GitHub rate limits.
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def search_repositories(query, limit):
    # Search GitHub repositories with pagination and de-duplication.
    items = []
    page = 1
    per_page = min(100, limit)
    seen = set()
    while len(items) < limit:
        url = (
            "https://api.github.com/search/repositories?"
            f"q={quote(query)}&sort=stars&order=desc&per_page={per_page}&page={page}"
        )
        data = fetch_json(url, headers=github_headers())
        if data.get("_error"):
            print(
                f"GitHub API error ({data.get('status')}): {data.get('message')}",
                file=sys.stderr,
            )
            break
        if "items" not in data:
            message = data.get("message", "Unexpected GitHub API response.")
            print(f"GitHub API error: {message}", file=sys.stderr)
            break
        if page == 1:
            total = data.get("total_count")
            if total is not None:
                print(f"  GitHub reported {total} total matches for query.")
        results = data.get("items", [])
        if not results:
            break
        for repo in results:
            repo_id = repo.get("id")
            if repo_id in seen:
                continue
            seen.add(repo_id)
            items.append(repo)
            if len(items) >= limit:
                break
        page += 1
    return items


def load_cache():
    if not CACHE_PATH.exists():
        return None
    try:
        data = json.loads(CACHE_PATH.read_text())
    except json.JSONDecodeError:
        return None
    return data


def save_cache(repos):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "repos": repos,
    }
    CACHE_PATH.write_text(json.dumps(payload))


def cache_is_fresh(cache):
    timestamp = cache.get("timestamp") if cache else None
    if not timestamp:
        return False
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return False
    cutoff = datetime.now(timezone.utc) - timedelta(days=CACHE_DAYS)
    return parsed >= cutoff


def collect_repos(max_results, min_stars, min_watchers, force_refresh):
    # Cache keeps API usage low for frequent runs.
    cache = load_cache()
    if cache and cache_is_fresh(cache) and not force_refresh:
        print("Using cached internship search results.")
        return cache.get("repos", [])

    repos = []
    for query in SEARCH_QUERIES:
        scoped_query = f"{query} stars:>={min_stars}"
        print(f"  Using query: {scoped_query}")
        results = search_repositories(scoped_query, max_results)
        repos.extend(results)
    unique = {repo["id"]: repo for repo in repos if repo.get("id")}
    repos = list(unique.values())
    save_cache(repos)
    print(f"  Query returned {len(repos)} repos.")
    if min_watchers <= 0:
        filtered = repos
    else:
        filtered = [repo for repo in repos if repo.get("watchers_count", 0) >= min_watchers]
    if min_stars > 0:
        filtered = [repo for repo in filtered if repo.get("stargazers_count", 0) >= min_stars]
    return filtered


def format_repo(repo):
    # Build a readable summary line for the output table.
    name = repo.get("full_name") or ""
    description = (repo.get("description") or "").strip()
    stars = repo.get("stargazers_count", 0)
    watchers = repo.get("watchers_count", 0)
    updated = (repo.get("updated_at") or "").split("T")[0]
    link = repo.get("html_url") or ""
    summary = description if description else "No description provided."
    details = f"{summary} (Stars: {stars}, Watchers: {watchers}, Updated: {updated})"
    return (name, details, link)


def write_output(repos):
    # Write a stable Markdown table so diffs stay readable.
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Internship Resources (GitHub)",
        "",
        f"_Last updated: {timestamp}_",
        "_Generated from GitHub repository search. Results are not endorsements; verify details in each repo._",
        "",
    ]
    if not repos:
        lines.extend(
            [
                "_No results found. Try lowering thresholds or using a token._",
                "",
            ]
        )
    lines.extend(
        [
        "| Repo | Description / Details | Link |",
        "| --- | --- | --- |",
        ]
    )
    for repo in repos:
        name, details, link = format_repo(repo)
        lines.append(f"| {name} | {details} | {link} |")
    OUTPUT_PATH.write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Update GitHub internship resource list.")
    parser.add_argument(
        "--max",
        type=int,
        default=DEFAULT_MAX_RESULTS,
        help="Maximum number of repositories to include.",
    )
    parser.add_argument(
        "--min-stars",
        type=int,
        default=DEFAULT_MIN_STARS,
        help="Minimum stars for repositories.",
    )
    parser.add_argument(
        "--min-watchers",
        type=int,
        default=DEFAULT_MIN_WATCHERS,
        help="Minimum watchers for repositories.",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Ignore cached search results and call the GitHub API.",
    )
    args = parser.parse_args()

    load_dotenv()
    print("Searching GitHub internship resources...")
    repos = collect_repos(args.max, args.min_stars, args.min_watchers, args.refresh)
    repos.sort(key=lambda r: (r.get("stargazers_count", 0), r.get("updated_at") or ""), reverse=True)
    write_output(repos)
    print(f"Updated {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
