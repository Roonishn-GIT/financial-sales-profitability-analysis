# Financial Sales & Profitability Analysis

End-to-end financial and sales analytics portfolio project using Excel, PostgreSQL, Python/Pandas, and Power BI.

## Business Objective
Analyze transaction-level sales data to identify the key drivers of revenue, cost, profitability, margin performance, product performance, customer value, regional performance, and time-based trends.

## Core Questions
- How are revenue, cost, profit, and margin trending over time?
- Which products and categories generate the most revenue and profit?
- Which products generate strong sales but weak margins?
- Who are the highest-value and most profitable customers?
- Which regions perform best and worst?
- Are there meaningful seasonal or month-over-month trends?
- Where should management focus to improve profitability?

## Tools
- **Excel:** source validation, formulas, PivotTables, and initial KPI checks
- **PostgreSQL:** querying, aggregations, CTEs, window functions, and KPI calculations
- **Python:** Pandas cleaning, EDA, descriptive statistics, correlations, and visualization
- **Power BI:** data model, DAX measures, and executive dashboard
- **Git/GitHub:** version control and project documentation

## Repository Structure
```text
data/
  raw/                 Original transaction-level source data
  cleaned/             Cleaned analysis-ready data
  data_dictionary.md   Field definitions and business meaning
excel/                 Excel validation and PivotTable workbook
sql/                   SQL setup, validation, KPI, customer, product, and trend queries
python/                Jupyter analysis and reusable scripts
powerbi/               Power BI dashboard files
visuals/               Exported charts and dashboard screenshots
documentation/         Business problem, methodology, findings, and executive summary
```

## Project Workflow
1. Validate the source data in Excel.
2. Load transaction data into PostgreSQL and calculate business KPIs with SQL.
3. Clean and analyze the dataset with Python/Pandas.
4. Build an executive Power BI dashboard.
5. Document findings, recommendations, and reproducible analysis in GitHub.

## Three-Day Build Plan
- **Day 1:** Dataset selection, business problem, Excel validation, database setup, and SQL analysis
- **Day 2:** Python cleaning, EDA, statistics, and visualization
- **Day 3:** Power BI dashboard, executive findings, recommendations, and portfolio polish

## Status
**In Progress — Day 1: Project setup and data acquisition**
