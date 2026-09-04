# Data Dictionary

Source file: `data/raw/product_sales_dataset_final.csv`

Validated grain: **one row = one transaction/order record**. The file contains **200,000 rows** with unique `Order_ID` values and no missing values or duplicate rows.

| Raw Field | Clean Field | Type | Description | Validation / Formula |
|---|---|---|---|---|
| Order_ID | order_id | Integer | Unique transaction/order identifier | 200,000 unique values; no duplicates |
| Order_Date | order_date | Date | Transaction date | 2023-01-01 through 2024-12-31 |
| Customer_Name | customer_name | Text | Customer name supplied by source | No separate customer ID is available; use name as analytical key |
| City | city | Text | U.S. city associated with transaction | 108 distinct cities |
| State | state | Text | U.S. state associated with transaction | 47 distinct states; Alaska, Hawaii, and North Carolina are absent |
| Region | region | Text | Sales region | Raw values: East, West, South, Centre; standardize `Centre` to `Central` in cleaned data |
| Country | country | Text | Country | All rows are United States |
| Category | category | Text | Product category | 4 distinct categories |
| Sub_Category | sub_category | Text | Product sub-category | 19 distinct sub-categories |
| Product_Name | product_name | Text | Product name | 49 distinct products |
| Quantity | quantity | Integer | Units sold in the transaction | Positive integer; used to validate revenue |
| ` Unit_Price ` | unit_price | Decimal/Currency | Selling price per unit | Trim whitespace from raw header; non-negative numeric |
| ` Revenue ` | revenue | Decimal/Currency | Transaction sales revenue | Validated as `quantity * unit_price` within rounding tolerance |
| ` Profit ` | profit | Decimal/Currency | Transaction profit | No negative-profit rows in source |

## Derived Analytical Fields

| Field | Type | Formula / Definition | Purpose |
|---|---|---|---|
| implied_cost | Decimal/Currency | `revenue - profit` | Cost proxy because raw COGS is not supplied |
| profit_margin_pct | Percentage | `profit / revenue` | Profitability efficiency |
| revenue_per_unit | Decimal/Currency | `revenue / quantity` | Revenue efficiency per unit |
| profit_per_unit | Decimal/Currency | `profit / quantity` | Profit contribution per unit |
| year | Integer | Year from `order_date` | YoY analysis |
| quarter | Text | Quarter from `order_date` | Quarterly trend analysis |
| month | Date/Text | Month from `order_date` | Monthly trend analysis |
| year_month | Text | `YYYY-MM` from `order_date` | Ordered monthly time-series analysis |

## Initial Validation Results

- Rows: **200,000**
- Columns: **14 raw fields**
- Date range: **2023-01-01 to 2024-12-31**
- Missing values: **0**
- Duplicate rows: **0**
- Duplicate `Order_ID`: **0**
- Revenue formula exceptions (`Quantity × Unit Price`): **0**
- Regions: **4**
- States: **47**
- Cities: **108**
- Categories: **4**
- Sub-categories: **19**
- Products: **49**
- Distinct customer names: **120,230**

## Raw Data Preservation Rule
The CSV in `data/raw/` must remain unchanged. Header cleanup, region standardization, date parsing, and derived financial fields belong in the cleaned dataset and downstream analytical layers.
