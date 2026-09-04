# Cleaned Data

**Status: Pending the Python phase.**

Analysis-ready exports will be written here after the programmatic cleaning rules are implemented and reconciled to the validated Excel/PostgreSQL controls.

The original source file in `data/raw/` must never be overwritten.

Planned cleaned-data rules include:

- normalized column names
- parsed dates
- standardized `Centre` → `Central`
- preserved numeric precision
- documented derived metrics such as implied cost and profit margin
- validation back to the **200,000-row** source and company financial controls
