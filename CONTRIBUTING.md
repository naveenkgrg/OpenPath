# Contributing

Thanks for improving this index. Please keep entries concise, link to authoritative sources, and prefer CNCF-hosted or project-owned references.

## Add or update entries
1) Choose the right folder: `data/good_first_issues/`, `data/mentorships/`, `data/internships/`, or `data/learning_resource/`.
2) Use the manual files (`manual_*.md`) for hand-curated additions so automation does not overwrite your changes.
3) Keep names and URLs accurate.
4) Use short descriptions (one line).

Manual files:
- `data/good_first_issues/manual_good_first_issues.md`
- `data/mentorships/manual_mentorships.md`
- `data/internships/manual_internship_resources.md`
- `data/learning_resource/manual_learning_resources.md`

## Data sources
- Add new sources to `data/sources.md`
- If the source is machine-readable, also add it to `config/sources.json`

## Running updates
Use the scripts referenced in `README.md` to refresh generated data.

## Maintainers
- Confirm generated files are up to date before merging.
- Ensure manual edits live in `manual_*.md`.
- Verify new skills in `config/skills.json` or `config/learning_skills.json` have valid fields.
