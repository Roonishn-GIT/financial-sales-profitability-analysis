# Financial Sales & Profitability Analysis

End-to-end financial analytics portfolio project using **Excel, PostgreSQL, Python/Pandas, Power BI, and Git/GitHub**.

## Project Status

- **Day 1 — Excel + PostgreSQL:** Complete and validated
- **Day 2 — Python/Pandas:** Next
- **Day 3 — Power BI + final portfolio polish:** Planned

The source contains **200,000 unique U.S. retail transactions** covering **2023-01-01 through 2024-12-31**.

## Business Objective

Analyze transaction-level sales data to identify the main drivers of revenue, implied cost, profit, margin performance, customer value, product performance, regional performance, and time-based trends. The final goal is to translate the analysis into practical recommendations for profitable growth.

## Validated Financial Controls

Excel and PostgreSQL were reconciled to the same headline totals.

| KPI | Validated Value |
|---|---:|
| Transactions / unique orders | 200,000 |
| Units sold | 370,800 |
| Revenue | $142,407,744.93 |
| Implied cost | $110,859,136.80 |
| Profit | $31,548,608.13 |
| Weighted profit margin | 22.15% |
| Minimum order date | 2023-01-01 |
| Maximum order date | 2024-12-31 |
| Duplicate Order_ID values | 0 |
| Revenue formula exceptions | 0 |

See [`documentation/day1_validation_audit.md`](documentation/day1_validation_audit.md) for the full Day 1 audit.

## Key Day 1 Findings

- **2024 grew modestly versus 2023:** revenue **+1.27%**, profit **+1.22%**, units **+0.86%**, and transactions **+0.39%**.
- **Electronics leads revenue** at **$57.49M** but has the lowest category margin at **14.03%**.
- **Home & Furniture produces the most profit** at **$11.22M** with a **23.53%** margin.
- **Accessories has the strongest category margin** at **34.00%**.
- **East leads regional revenue** at **$44.98M**, while **South has the strongest regional margin** at **23.58%**.
- Several high-revenue Electronics products cluster around a ~14% margin, indicating a broader category-level margin issue rather than a single-product anomaly.

## Tools

- **Excel:** source validation, calculated controls, PivotTables, and initial charts
- **PostgreSQL / DBeaver:** staging, typed tables, validation, CTEs, window functions, rankings, running totals, moving averages, and trend analysis
- **Python:** Pandas cleaning, EDA, statistics, and visualization *(next phase)*
- **Power BI:** DAX measures and executive dashboard *(planned)*
- **Git/GitHub:** version control, documentation, and portfolio presentation

## Repository Structure

```text
data/
  raw/                 Original source CSV — preserved unchanged
  cleaned/             Analysis-ready exports created during Python phase
  data_dictionary.md   Field definitions, validation rules, and derived metrics
excel/
  financial_sales_analysis.xlsx
sql/
  01_database_setup.sql
  01b_data_load.sql
  02_data_validation.sql
  03_kpi_analysis.sql
  04_customer_analysis.sql
  05_product_analysis.sql
  06_trend_analysis.sql
python/
  scripts/              Python analysis scaffolding and reusable helpers
powerbi/                Power BI deliverables
visuals/                Exported charts and dashboard screenshots
documentation/          Business problem, methodology, findings, audit, and summary
```

## SQL Reproduction Order

> **Important:** `01_database_setup.sql` is destructive by design because it drops and recreates the project tables. Run it only when intentionally rebuilding the database from scratch.

1. Run `sql/01_database_setup.sql`.
2. Import `data/raw/product_sales_dataset_final.csv` into `sales_stage`.
3. Confirm `sales_stage` contains **200,000** rows.
4. Run `sql/01b_data_load.sql` **once** to populate `sales_transactions`.
5. Run `sql/02_data_validation.sql` and confirm the validated controls above.
6. Run `sql/03_kpi_analysis.sql` through `sql/06_trend_analysis.sql`.

Detailed import notes and expected outputs are documented in [`sql/README.md`](sql/README.md).

## Documentation

- [`documentation/business_problem.md`](documentation/business_problem.md) — business context and KPI framework
- [`documentation/methodology.md`](documentation/methodology.md) — completed and planned analytical workflow
- [`documentation/findings.md`](documentation/findings.md) — validated Day 1 findings
- [`documentation/executive_summary.md`](documentation/executive_summary.md) — current management summary
- [`documentation/day1_validation_audit.md`](documentation/day1_validation_audit.md) — cross-tool quality-control audit

## Next Phase

The Python phase will reproduce the SQL controls, perform deeper EDA/statistical analysis, evaluate distributions and outliers, and export portfolio-ready visualizations before the final Power BI dashboard is built.
