#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "learning_resource"
SKILLS_PATH = ROOT / "config" / "learning_skills.json"
CACHE_DIR = ROOT / ".cache"
CACHE_PATH = CACHE_DIR / "learning_resources.json"

USER_AGENT = "cncf-opportunities-updater/1.0"
DEFAULT_MAX_REPOS = int(os.environ.get("LEARN_MAX_REPOS", "15"))
DEFAULT_MIN_STARS = int(os.environ.get("LEARN_MIN_STARS", "100"))
DEFAULT_MAX_VIDEOS = int(os.environ.get("LEARN_MAX_VIDEOS", "10"))
DEFAULT_MIN_VIEWS = int(os.environ.get("LEARN_MIN_VIEWS", "1000"))
DEFAULT_MIN_LIKES = int(os.environ.get("LEARN_MIN_LIKES", "100"))
CACHE_DAYS = int(os.environ.get("LEARN_CACHE_DAYS", "7"))


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


def fetch_json(url, headers=None):
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
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def load_skills():
    if not SKILLS_PATH.exists():
        raise FileNotFoundError(f"Missing skills file: {SKILLS_PATH}")
    skills = json.loads(SKILLS_PATH.read_text())
    if not isinstance(skills, list):
        raise ValueError("config/learning_skills.json must be a list")
    for skill in skills:
        if not isinstance(skill, dict):
            raise ValueError("Each skill must be an object")
        for field in ("name", "filename", "keywords"):
            if field not in skill or not skill[field]:
                raise ValueError(f"Skill missing required field: {field}")
    return skills


def load_cache():
    if not CACHE_PATH.exists():
        return None
    try:
        return json.loads(CACHE_PATH.read_text())
    except json.JSONDecodeError:
        return None


def save_cache(data):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data,
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
    cutoff = datetime.now(timezone.utc).timestamp() - (CACHE_DAYS * 86400)
    return parsed.timestamp() >= cutoff


def search_github_repos(query, limit):
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
            break
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


def format_repo(repo):
    name = repo.get("full_name") or ""
    description = (repo.get("description") or "").strip() or "No description provided."
    stars = repo.get("stargazers_count", 0)
    updated = (repo.get("updated_at") or "").split("T")[0]
    link = repo.get("html_url") or ""
    details = f"{description} (Stars: {stars}, Updated: {updated})"
    return (name, details, link)


def youtube_api_key():
    return os.environ.get("YOUTUBE_API_KEY")


def fetch_youtube_videos(query, max_results):
    api_key = youtube_api_key()
    if not api_key:
        return []
    search_url = (
        "https://www.googleapis.com/youtube/v3/search?"
        f"part=snippet&type=video&maxResults={max_results}"
        f"&q={quote(query)}&key={api_key}"
    )
    data = fetch_json(search_url)
    if data.get("_error"):
        return []
    video_ids = [item.get("id", {}).get("videoId") for item in data.get("items", [])]
    video_ids = [vid for vid in video_ids if vid]
    if not video_ids:
        return []
    stats_url = (
        "https://www.googleapis.com/youtube/v3/videos?"
        f"part=snippet,statistics&id={quote(','.join(video_ids))}&key={api_key}"
    )
    stats = fetch_json(stats_url)
    if stats.get("_error"):
        return []
    return stats.get("items", [])


def format_video(video):
    snippet = video.get("snippet", {})
    stats = video.get("statistics", {})
    title = snippet.get("title", "")
    channel = snippet.get("channelTitle", "")
    video_id = video.get("id", "")
    views = int(stats.get("viewCount", 0))
    likes = int(stats.get("likeCount", 0)) if "likeCount" in stats else 0
    link = f"https://www.youtube.com/watch?v={video_id}" if video_id else ""
    details = f"{channel} (Views: {views}, Likes: {likes})"
    return (title, details, link, views, likes)


def write_skill_file(skill, repos, videos, timestamp):
    path = DATA_DIR / skill["filename"]
    lines = [
        f"# Learning Resources: {skill['name']}",
        "",
        f"_Last updated: {timestamp}_",
        "",
        "## GitHub Repositories",
        "",
        "| Repo | Description / Details | Link |",
        "| --- | --- | --- |",
    ]
    if not repos:
        lines.append("| _No results_ | _Try adjusting thresholds_ | _N/A_ |")
    for repo in repos:
        name, details, link = format_repo(repo)
        lines.append(f"| {name} | {details} | {link} |")

    lines.extend([
        "",
        "## YouTube Videos",
        "",
        "| Title | Channel / Stats | Link |",
        "| --- | --- | --- |",
    ])
    if not videos:
        lines.append("| _No results or no API key_ | _Set YOUTUBE_API_KEY to enable_ | _N/A_ |")
    for video in videos:
        title, details, link, _, _ = format_video(video)
        lines.append(f"| {title} | {details} | {link} |")

    path.write_text("\n".join(lines) + "\n")


def collect_learning_resources(skills, max_repos, min_stars, max_videos, min_views, min_likes, force_refresh):
    cache = load_cache()
    if cache and cache_is_fresh(cache) and not force_refresh:
        print("Using cached learning resource results.")
        return cache.get("data", {})

    data = {}
    for skill in skills:
        print(f"Fetching resources for {skill['name']}...")
        keyword_query = " OR ".join(skill["keywords"])
        repo_query = f"({keyword_query}) in:name,description,readme stars:>={min_stars}"
        print(f"  Repo query: {repo_query}")
        repos = search_github_repos(repo_query, max_repos)
        print(f"  Found {len(repos)} repositories.")
        videos = []
        if youtube_api_key():
            print("  Searching YouTube...")
            raw_videos = fetch_youtube_videos(f"{skill['name']} tutorial", max_videos)
            for video in raw_videos:
                _, _, _, views, likes = format_video(video)
                if views >= min_views and likes >= min_likes:
                    videos.append(video)
            print(f"  Found {len(videos)} videos after filtering.")
        else:
            print("  Skipping YouTube (YOUTUBE_API_KEY not set).")
        data[skill["name"]] = {"repos": repos, "videos": videos}

    save_cache(data)
    return data


def main():
    parser = argparse.ArgumentParser(description="Update skill-based learning resources.")
    parser.add_argument("--max-repos", type=int, default=DEFAULT_MAX_REPOS)
    parser.add_argument("--min-stars", type=int, default=DEFAULT_MIN_STARS)
    parser.add_argument("--max-videos", type=int, default=DEFAULT_MAX_VIDEOS)
    parser.add_argument("--min-views", type=int, default=DEFAULT_MIN_VIEWS)
    parser.add_argument("--min-likes", type=int, default=DEFAULT_MIN_LIKES)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    load_dotenv()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    skills = load_skills()
    print(f"Loaded {len(skills)} skills.")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    data = collect_learning_resources(
        skills,
        args.max_repos,
        args.min_stars,
        args.max_videos,
        args.min_views,
        args.min_likes,
        args.refresh,
    )

    for skill in skills:
        entry = data.get(skill["name"], {"repos": [], "videos": []})
        write_skill_file(skill, entry.get("repos", []), entry.get("videos", []), timestamp)

    print(f"Updated {DATA_DIR}")


if __name__ == "__main__":
    main()
