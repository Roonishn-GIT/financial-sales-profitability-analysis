# Validated Findings

The findings below were produced during Day 1 and reconciled across Excel and PostgreSQL where applicable.

## 1. Company-Level Performance

- Transactions / unique orders: **200,000**
- Units sold: **370,800**
- Revenue: **$142,407,744.93**
- Profit: **$31,548,608.13**
- Implied cost: **$110,859,136.80**
- Weighted profit margin: **22.15%**
- Date range: **2023-01-01 to 2024-12-31**

The core totals match between the Excel validation workbook and PostgreSQL.

## 2. Year-over-Year Performance

| Year | Transactions | Units | Revenue | Profit | Margin |
|---|---:|---:|---:|---:|---:|
| 2023 | 99,807 | 184,609 | $70,755,372.66 | $15,678,961.99 | 22.16% |
| 2024 | 100,193 | 186,191 | $71,652,372.27 | $15,869,646.14 | 22.15% |

2024 versus 2023:

- Transactions: **+0.39%**
- Units sold: **+0.86%**
- Revenue: **+1.27%**
- Profit: **+1.22%**

Revenue and profit grew, but the weighted profit margin remained essentially flat.

## 3. Product Categories

| Category | Revenue | Profit | Margin |
|---|---:|---:|---:|
| Electronics | $57,485,698.06 | $8,065,113.92 | 14.03% |
| Home & Furniture | $47,674,426.96 | $11,218,596.44 | 23.53% |
| Clothing & Apparel | $27,134,365.30 | $8,826,851.49 | 32.53% |
| Accessories | $10,113,254.61 | $3,438,046.28 | 34.00% |

Key product insight: **Electronics contributes the most revenue but has the lowest category margin.** Several major Electronics products also cluster around a ~14% margin, indicating that the profitability issue is broad within the category.

Home & Furniture generates the highest total profit, while Accessories and Clothing & Apparel are the strongest margin categories.

## 4. Regional Performance

| Region | Revenue | Profit | Margin | Revenue Share |
|---|---:|---:|---:|---:|
| East | $44,980,048.22 | $9,221,327.43 | 20.50% | 31.59% |
| West | $36,242,841.73 | $8,313,962.76 | 22.94% | 25.45% |
| Central | $36,081,894.34 | $8,094,863.77 | 22.43% | 25.34% |
| South | $25,102,960.64 | $5,918,454.17 | 23.58% | 17.63% |

East leads revenue, but South has the strongest margin. This creates a useful comparison between scale and profitability efficiency.

## 5. Customer Analysis

- Customer analysis uses the supplied `Customer_Name` field because the source does not contain a separate customer ID.
- Revenue and profit rankings were calculated with SQL window functions.
- Some customers show large gaps between revenue rank and profit rank, demonstrating that revenue alone is not a sufficient measure of customer value.
- The Top 10 revenue analysis built in Excel was reproduced as a dedicated SQL query for independent verification.

## 6. Trend Analysis

- The monthly dataset is complete across 24 months from January 2023 through December 2024.
- Month-over-month growth uses `LAG()`; the first month correctly returns `NULL` because no prior month exists.
- Running revenue/profit totals and 3-month moving averages were implemented using window functions.
- Calendar-month seasonality is aggregated across both years and will be explored further in Python.

## 7. Data Quality

- Duplicate `Order_ID` values: **0**
- Missing required values: **0**
- Revenue formula exceptions (`Quantity × Unit Price` outside tolerance): **0**
- Raw region value `Centre` is standardized to `Central` in the analytical table.
- The raw CSV remains unchanged.

## Interpretation

Day 1 establishes a reliable analytical foundation: company totals reconcile, dimensional totals roll back to the same company totals, and the SQL analytical layer reproduces the Excel findings while adding reusable ranking and time-series logic.
