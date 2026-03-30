# Analysis Workspace

This folder is for pulling a bounded slice of MongoDB data into pandas and exploring it in notebooks.

## Setup

1. Copy `analysis/.env.example` to `analysis/.env`.
2. Put your real `MONGO_DB_URL` into `analysis/.env`.
3. Install dependencies from this folder.
4. Start JupyterLab and open notebooks in `analysis/notebooks`.

## Environment variables

- `MONGO_DB_URL`: MongoDB Atlas connection string.
- `MONGO_DB_NAME` (optional): defaults to `TrainDelaysDB`.

## Suggested notebook flow

1. `01_data_pull_and_schema.ipynb`
   - Connect to MongoDB.
   - Pull a small, time-bounded sample.
   - Inspect schema and null rates.
2. `02_delay_exploration.ipynb`
   - Build delay features.
   - Explore delay distributions by train type and hour.

## Notes

- Main source collection is `trainStateSnaphots` (existing project naming).
- Pull only a limited window (for example, last 24h or 7d), not the full collection.
