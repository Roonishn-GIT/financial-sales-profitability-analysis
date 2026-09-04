# Excel Analysis

`financial_sales_analysis.xlsx` is the completed Day 1 Excel validation and exploratory-analysis workbook.

## Completed Work

- Converted the source data into a structured Excel table.
- Added derived financial controls, including implied cost and profit-margin calculations.
- Built a validation summary for row counts, revenue, profit, implied cost, margin, units, dates, duplicates, and revenue-formula exceptions.
- Built PivotTable analyses for year, product category/sub-category, region, and top customers.
- Added presentation-ready charts for annual, category, regional, and customer performance.

## Reconciled Headline Values

| KPI | Value |
|---|---:|
| Rows / unique orders | 200,000 |
| Units sold | 370,800 |
| Revenue | $142,407,744.93 |
| Profit | $31,548,608.13 |
| Implied cost | $110,859,136.80 |
| Weighted profit margin | 22.15% |
| Date range | 2023-01-01 to 2024-12-31 |

These values were independently reproduced in PostgreSQL during Day 1.

## Notes

- The original CSV remains unchanged in `data/raw/`.
- Any Excel lock file beginning with `~$` is temporary and should never be committed.
- The workbook is a portfolio deliverable; SQL, Python, and Power BI provide independent analytical layers rather than replacing the Excel work.
