# Contributing

Thanks for improving this index. Please keep entries concise, link to authoritative sources, and prefer CNCF-hosted or project-owned references.

## Add or update entries
- Edit the relevant file in `data/`
- Keep names and URLs accurate
- Use short descriptions (one line)

## Data sources
- Add new sources to `data/sources.md`
- If the source is machine-readable, also add it to `config/sources.json`

## Running updates
To refresh `data/projects.md` from the CNCF Landscape:

```bash
python3 scripts/update_data.py
```
