# Data dictionary (analysis)

## Canonical station coordinates

- File: `analysis/data/derived/station_coords.csv`
- Status: canonical station coordinate mapping for analysis workflows.

Columns:

- `name`: station name label.
- `lat`: latitude in decimal degrees.
- `lon`: longitude in decimal degrees.
- `n_samples`: number of samples used to estimate coordinates.
- `lat_spread`: latitude spread across samples.
- `lon_spread`: longitude spread across samples.

## Deprecated mapping

- File: `analysis/data/derived/archive/station_mapping.csv`
- Status: deprecated; retained only for historical comparisons and debugging.
