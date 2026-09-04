# PostgreSQL Analysis Guide

This folder contains the complete Day 1 PostgreSQL workflow for the Financial Sales & Profitability Analysis project.

## Run Order

### 1. Build the schema

Run:

```text
01_database_setup.sql
```

> **Warning:** this script is intentionally destructive. It drops and recreates `sales_stage`, `sales_transactions`, and `sales_enriched`. Do not rerun it after loading data unless you intend to rebuild the database from scratch.

### 2. Import the raw CSV into `sales_stage`

Source:

```text
data/raw/product_sales_dataset_final.csv
```

The raw CSV has whitespace in the final three header names. In DBeaver, manually map them to the existing staging columns:

| Raw CSV Header | Target Column |
|---|---|
| ` Unit_Price ` | `unit_price` |
| ` Revenue ` | `revenue` |
| ` Profit ` | `profit` |

All 14 fields should map to **existing** target columns before the import is completed.

Then verify:

```sql
SELECT COUNT(*) AS staging_rows
FROM sales_stage;
```

Expected result: **200,000**.

### 3. Load the typed analytical table

Run:

```text
01b_data_load.sql
```

This script:

- Parses `Order_Date` into a PostgreSQL `DATE`.
- Trims text fields.
- Standardizes `Centre` to `Central`.
- Loads `sales_transactions`.

Run the load script only after `sales_stage` contains the expected 200,000 rows.

Expected final count: **200,000**.

### 4. Validate the data

Run:

```text
02_data_validation.sql
```

Expected headline controls:

| KPI | Expected |
|---|---:|
| Rows | 200,000 |
| Unique orders | 200,000 |
| Duplicate Order_ID | 0 |
| Units | 370,800 |
| Revenue | $142,407,744.93 |
| Profit | $31,548,608.13 |
| Implied cost | $110,859,136.80 |
| Weighted margin | 22.15% |
| Minimum date | 2023-01-01 |
| Maximum date | 2024-12-31 |
| Revenue formula exceptions | 0 |

### 5. Run the analysis scripts

Run each file in order:

```text
03_kpi_analysis.sql
04_customer_analysis.sql
05_product_analysis.sql
06_trend_analysis.sql
```

These files demonstrate:

- Aggregations and KPI calculations
- CTEs
- `LAG()`
- `RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()`
- `PARTITION BY`
- Contribution percentages
- Running totals
- Moving averages
- Month-over-month and year-over-year growth

## Expected NULL Values

A `NULL` growth rate in the first month/year is expected because `LAG()` has no prior period to compare against. It is not a missing-data error.

## Data Model

- `sales_stage` — raw-import staging table
- `sales_transactions` — typed analytical fact table
- `sales_enriched` — reusable view with implied cost, margin, per-unit KPIs, year, quarter, and month

## Important Derived Measures

```text
Implied Cost = Revenue - Profit
Profit Margin = Profit / Revenue
Revenue per Unit = Revenue / Quantity
Profit per Unit = Profit / Quantity
```
