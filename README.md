# Slovak Train Delay Prediction

Pipeline and analysis workspace for collecting, processing, and exploring Slovak railway delay data.

## Project structure

- `data_gathering/`: pulls live train state snapshots and writes them to MongoDB.
- `data_processing/`: transforms gathered data and builds graph-oriented artifacts.
- `timetable_downloader/`: downloads timetable-related supporting data.
- `analysis/`: exploratory analysis and visualization from exported Parquet data.

## Analysis quick links

- Workspace guide: `analysis/README.md`
- Canonical station coordinates: `analysis/data/derived/station_coords.csv`
- External raw snapshot export: `analysis/data/train_data.parquet`

## Data and secrets policy

- Keep secrets only in local `.env` files.
- Do not commit hardcoded database URIs or credentials.
- Treat large raw data exports as external artifacts unless explicitly intended for version control.
