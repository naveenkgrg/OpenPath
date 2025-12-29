# CNCF Opportunities Index

Static, human-friendly lists of CNCF-focused internships, mentorships, first-time issues, and skill-based contribution paths. Includes a simple script to refresh CNCF project data from public sources.

## What's inside
- `data/projects.md` CNCF projects (auto-generated from CNCF Landscape data)
- `data/projects_manual.md` hand-curated CNCF projects and notes
- `data/internships.md` internship programs and links
- `data/mentorships.md` mentorship programs and links
- `data/first_time_issues.md` beginner-friendly issues or labels
- `data/good_first_issues/` skill-based good first issues (auto-generated)
- `data/skill_based_projects.md` projects grouped by skills
- `data/sources.md` authoritative sources used by this repo

## Quick start
- Read the lists in `data/`
- Add or edit entries via pull request

This is an open source index. Listings are generated from public sources and GitHub label searches (for example `good first issue`), so inclusion is not a personal recommendation and labels can vary by project. Before contributing, review each project's contribution guidelines and scope, and confirm the issue is a good fit.

Disclaimer: Issues can close or change quickly, labels are project-specific (not a guarantee of difficulty), and this index does not endorse or vet projects. Always verify current status and use your own judgment.

## Update CNCF project list
This updates `data/projects.md` from the CNCF Landscape JSON.

```bash
python3 scripts/update_data.py
```

## Update mentorships, internships, and first-time issues
This updates `data/mentorships.md`, `data/internships.md`, `data/first_time_issues.md`, and `data/good_first_issues/` from LFX Mentorship, CNCF Landscape data, and GitHub Search.

Skill queries live in `config/skills.json` and can be updated via PR to add or refine categories.

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

## Contributing
See `CONTRIBUTING.md` for how to add new entries or sources.
