# Analysis Workspace

This folder contains exploratory analysis built on an externally exported MongoDB snapshot in Parquet format.

## Canonical files

- Correct station coordinate mapping: `analysis/data/derived/station_coords.csv`
- Raw imported dataset: `analysis/data/raw/train_data.parquet`
- Legacy/archived mapping (kept for reference only): `analysis/data/derived/archive/station_mapping.csv`

## Folder layout

```
analysis/
  notebooks/            # exploratory notebooks
  scripts/              # helper scripts
  data/
  outputs/maps/         # exported HTML network maps
  docs/                 # analysis notes
```

## Setup

From `analysis/`:

1. Install dependencies: `uv sync`
2. Start notebook server: `uv run jupyter lab`
3. Open notebooks in `analysis/notebooks/`

## Workflow

1. Load `data/train_data.parquet`.
2. Parse and transform train snapshot payloads.
3. Build features and network graph artifacts.
4. Export outputs into `data/` and `outputs/maps/`.

## Security note

- Do not store hardcoded database credentials in notebooks or scripts.
- Use local environment variables (`.env`) for secrets.
