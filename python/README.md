# Python Analysis

**Status: Complete and validated.**

The Python workflow cleans the source data, validates it against the Day 1 Excel/PostgreSQL controls, performs exploratory profitability analysis, and exports five Matplotlib charts.

## Scripts

- `python/scripts/clean_data.py` standardizes column names, parses dates, confirms numeric fields, standardizes `Centre` to `Central`, and creates analysis-ready profitability fields.
- `python/scripts/validate_cleaned_data.py` checks data quality and reconciles the cleaned dataset to the exact Day 1 controls with readable PASS/FAIL output.
- `python/scripts/analysis.py` calculates overall, yearly, category, regional, customer, monthly, and product-margin results; reconciles key outputs to SQL; and creates the portfolio charts.

## Run from the Repository Root

```bash
python python/scripts/clean_data.py
python python/scripts/validate_cleaned_data.py
python python/scripts/analysis.py
```

The cleaning script writes the analysis-ready dataset to `data/cleaned/financial_sales_cleaned.csv`. The original file in `data/raw/` is read-only for this workflow and is never modified.
