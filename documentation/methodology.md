# Methodology

This project uses multiple analytical tools on the same source data so that headline KPIs can be independently reproduced and reconciled.

## 1. Source Preservation and Data Definition — Complete

- The original CSV is stored in `data/raw/` and is not modified.
- The validated grain is **one row = one transaction/order record**.
- `Order_ID` is unique across all **200,000** rows.
- A data dictionary documents raw fields, cleaned names, business definitions, and derived metrics.

## 2. Excel Validation and Exploratory Analysis — Complete

Excel was used as the first independent control layer.

Completed work includes:

- Structured-table conversion of the source data.
- Row-count and uniqueness checks.
- Revenue, profit, implied-cost, margin, and units controls.
- Date-range validation.
- Revenue recalculation checks using `Quantity × Unit Price`.
- PivotTable analysis by year, product category/sub-category, region, and customer.
- Presentation-ready charts for the major business dimensions.

The final Excel controls reconcile to the PostgreSQL totals.

## 3. PostgreSQL Data Model and Validation — Complete

The SQL workflow uses a staging-to-typed-table pattern:

1. `sales_stage` receives the raw CSV structure.
2. `sales_transactions` stores typed, analysis-ready records.
3. `Centre` is standardized to `Central` during the load.
4. `sales_enriched` exposes derived fields such as implied cost, margin, year, quarter, and month.
5. Indexes support common date, category, region, state, and customer queries.

Validation includes:

- Row and unique-order counts.
- Duplicate checks.
- Core financial reconciliation.
- Date-range checks.
- Revenue-formula exception checks.
- Missing-value checks.
- Region-cleanup verification.
- Basic financial range checks.

## 4. PostgreSQL Analytical Layer — Complete

The SQL analysis includes:

- Executive KPIs and annual performance.
- Year-over-year growth using CTEs and `LAG()`.
- Customer performance, rankings, concentration, and rank-gap analysis.
- Category, product, and sub-category profitability analysis.
- Aggregate window functions for contribution percentages.
- Monthly growth, running totals, and 3-month moving averages.
- Regional contribution and ranking.
- Calendar-month seasonality analysis.

## 5. Python Analysis — Complete

The completed Python workflow follows a reproducible sequence:

1. **Cleaning:** Normalize column names, parse dates, standardize the Central region, confirm numeric fields, and create derived profitability measures without changing the raw CSV.
2. **Validation:** Check required fields, duplicates, regions, country, the revenue formula, dates, and exact Day 1 control totals.
3. **Reconciliation:** Reproduce company, annual, category, and regional results from the Excel/PostgreSQL validation layer.
4. **EDA:** Analyze overall KPIs, year-over-year results, categories, regions, customer-name labels, monthly trends, and product margins.
5. **Visualization:** Export five portfolio-ready Matplotlib charts from the cleaned dataset.

Profit margin is calculated as a weighted measure: total profit divided by total revenue. This avoids giving small and large transactions equal influence. Customer analysis groups the supplied `Customer_Name` label because no unique customer ID exists; results must not be interpreted as verified individual-customer identities.

## 6. Power BI — Planned

Power BI will provide the executive reporting layer with:

- Validated DAX measures.
- Interactive trend, product, customer, and regional views.
- Executive KPI cards and filters.
- Dashboard screenshots for the portfolio README.

## 7. Recommendation Framework

Recommendations will be tied to quantified evidence and will distinguish between revenue scale, absolute profit, and margin efficiency. The executive summary incorporates the validated Excel, PostgreSQL, and Python results; final recommendations will also incorporate the planned Power BI phase.
