# CNCF Opportunities Index

Static, human-friendly lists of CNCF-focused internships, mentorships, and first-time issues. Includes scripts to refresh data from public sources.

## What's inside
- `data/good_first_issues/` good first issue lists (auto-generated) + manual additions
- `data/mentorships/` mentorship programs and manual notes
- `data/internships/` internship programs, resources, and manual notes
- `data/internships/success_stories.md` community success stories
- `data/mentorships/reach_out.md` guidance for contacting maintainers or mentors
- `data/learning_resource/` skill-based learning resources (auto-generated) + manual additions
- `data/sources.md` authoritative sources used by this repo

## Quick start
- Read the lists in `data/`
- Add or edit entries via pull request

This is an open source index. Listings are generated from public sources and GitHub label searches (for example `good first issue`), so inclusion is not a personal recommendation and labels can vary by project. Before contributing, review each project's contribution guidelines and scope, and confirm the issue is a good fit.

Disclaimer: Issues can close or change quickly, labels are project-specific (not a guarantee of difficulty), and this index does not endorse or vet projects. Always verify current status and use your own judgment.

If this project helps you land an internship, job, or meaningful contribution, please share your story in `data/internships/success_stories.md`.

## Update mentorships, internships, and first-time issues
This updates `data/mentorships/mentorships.md`, `data/internships/internships.md`, `data/good_first_issues/first_time_issues.md`, and `data/good_first_issues/` from LFX Mentorship, CNCF Landscape data, and GitHub Search.

Skill queries live in `config/skills.json` and can be updated via PR to add or refine categories.
Learning resource skills live in `config/learning_skills.json`.

```bash
python3 scripts/update_opportunities.py
```

If you hit GitHub rate limits, set a token:

```bash
GITHUB_TOKEN=... python3 scripts/update_opportunities.py
```

You can also store `GITHUB_TOKEN` in a local `.env` file.

Good first issues are sorted by repo popularity (stars) and then most recently updated.

To increase good first issue count (default 200):

```bash
GOOD_FIRST_MAX=300 python3 scripts/update_opportunities.py
```

To force refresh (otherwise refreshes if older than 7 days):

```bash
python3 scripts/update_opportunities.py --refresh
```

To refresh a single skill file:

```bash
python3 scripts/update_opportunities.py --skill "Python"
```

To increase LFX pagination (default 10 pages):

```bash
LFX_MAX_PAGES=50 python3 scripts/update_opportunities.py
```

## Update internship resources from GitHub
This searches GitHub repositories that list internship resources and writes `data/internships/internship_resources.md`.

```bash
python3 scripts/update_internship_resources.py
```

To adjust thresholds:

```bash
INTERNSHIP_MAX=150 INTERNSHIP_MIN_STARS=100 INTERNSHIP_MIN_WATCHERS=100 \
python3 scripts/update_internship_resources.py
```

To force a fresh GitHub search (skip cache):

```bash
python3 scripts/update_internship_resources.py --refresh
```

## Update learning resources
This generates skill-based learning resources under `data/learning_resource/` using GitHub search and optional YouTube data.

```bash
python3 scripts/update_learning_resources.py
```

To override defaults:

```bash
LEARN_MAX_REPOS=20 LEARN_MIN_STARS=100 LEARN_MAX_VIDEOS=10 LEARN_MIN_VIEWS=1000 LEARN_MIN_LIKES=100 \
python3 scripts/update_learning_resources.py
```

To enable YouTube results, set `YOUTUBE_API_KEY` in `.env`.

## Contributing
See `CONTRIBUTING.md` for how to add new entries or sources.

## How to contribute (quick guide)
1) Pick the right folder: `data/good_first_issues/`, `data/mentorships/`, `data/internships/`, or `data/learning_resource/`.
2) For manual updates, use the `manual_*.md` files in each folder so automation does not overwrite your changes.
3) Keep entries concise, link to authoritative sources, and verify the info before submitting a PR.
4) If you add a new skill category, update `config/skills.json` (good first issues) or `config/learning_skills.json` (learning resources).
5) Run the relevant script to regenerate auto files if your change affects generated content.

## For maintainers
- Ensure auto-generated files are updated via scripts before merging.
- Confirm manual edits are placed in `manual_*.md` files.
- Validate new skill entries include `name`, `filename`, and a sensible query/keywords.
