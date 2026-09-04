# Day 1 Validation Audit

**Audit date:** 2026-09-04  
**Scope:** Excel workbook, PostgreSQL load/validation, SQL analytical outputs, and repository structure.

## Audit Result

**PASS — Day 1 analytical controls are internally consistent and the core Excel/PostgreSQL values reconcile.**

## Repository Assets Verified

- Raw CSV exists at `data/raw/product_sales_dataset_final.csv`.
- Excel workbook exists at `excel/financial_sales_analysis.xlsx`.
- SQL setup, load, validation, KPI, customer, product, and trend scripts are present in `sql/`.
- No Excel temporary lock file (`~$...`) is present in the repository.
- At the time of the Day 1 audit, the Python and Power BI phases had not started. Python Day 2 has since been completed and validated; Power BI remains planned.

## Database Load Verification

Final DBeaver checks confirmed:

| Table | Row Count |
|---|---:|
| `sales_stage` | 200,000 |
| `sales_transactions` | 200,000 |

The typed transaction table successfully loaded after the raw staging import.

## Cross-Tool Financial Reconciliation

| Control | Excel / SQL Result |
|---|---:|
| Row count | 200,000 |
| Unique Order_ID | 200,000 |
| Duplicate Order_ID | 0 |
| Units sold | 370,800 |
| Total revenue | $142,407,744.93 |
| Total profit | $31,548,608.13 |
| Implied cost | $110,859,136.80 |
| Weighted profit margin | 22.15% |
| Minimum date | 2023-01-01 |
| Maximum date | 2024-12-31 |
| Revenue formula exceptions | 0 |

## Independent Roll-Up Checks

### Annual totals

2023 + 2024 revenue equals **$142,407,744.93** and profit equals **$31,548,608.13**, matching the company controls.

### Category totals

The four category revenue values sum exactly to **$142,407,744.93** and category profit sums to **$31,548,608.13**.

### Regional totals

East + West + Central + South revenue sums exactly to **$142,407,744.93** and regional profit sums to **$31,548,608.13**.

These independent dimensional roll-ups provide an additional consistency check beyond the headline aggregation.

## Year-over-Year Calculation Check

The SQL `LAG()` calculations were mathematically checked against the annual totals:

- Transactions: **+0.39%**
- Units: **+0.86%**
- Revenue: **+1.27%**
- Profit: **+1.22%**

## Expected Non-Error Values

- The first row of a month-over-month `LAG()` comparison returns `NULL` because there is no prior month. This is expected and is **not** a data error.
- The 2023 row in year-over-year growth likewise has no prior-year growth percentage. This is expected.
- `Implied Cost` is a derived measure (`Revenue - Profit`) because raw COGS is not supplied.

## SQL Script Review

- `01_database_setup.sql` executed successfully and creates staging/final tables, analytical view, and indexes.
- `01b_data_load.sql` successfully transformed the final 200,000 staging rows into the typed transaction table.
- `02_data_validation.sql` contains the reconciliation and quality checks used for the validated controls.
- `03_kpi_analysis.sql` executed successfully, including annual KPIs and YoY `LAG()` logic.
- `04_customer_analysis.sql` executed successfully, including ranking and rank-gap window functions.
- `05_product_analysis.sql` executed successfully and reconciled category totals to Excel.
- `06_trend_analysis.sql` executed successfully, including MoM growth, running totals, rolling averages, regional rankings, and seasonality.

## Safety Note

`01_database_setup.sql` intentionally contains `DROP` statements. It must only be run when intentionally rebuilding the database from scratch. Running it after importing `sales_stage` will delete the imported staging rows.

## Remaining Work at the End of Day 1

The following were future phases when this Day 1 audit was completed:

- Python/Pandas cleaning, validation, EDA, and chart exports — **completed during Day 2**.
- Cleaned-data export in `data/cleaned/` — **completed during Day 2**.
- Power BI dashboard and DAX measures.
- Final portfolio screenshots and fully finalized recommendations.

## Conclusion

Day 1 is complete. The source data, Excel controls, database load, company KPIs, category totals, regional totals, and SQL time-series logic are consistent with the validated results observed during the build.
