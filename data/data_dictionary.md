# Data Dictionary

The final field definitions will be populated after the transaction dataset is selected and validated.

| Field | Type | Description | Validation / Formula |
|---|---|---|---|
| transaction_id | TBD | Unique transaction or line identifier | Must be unique at chosen grain |
| order_date | Date | Transaction/order date | Valid date range |
| customer | Text | Customer identifier or name | Check missing values |
| product | Text | Product identifier or name | Check missing values |
| category | Text | Product category | Standardize labels |
| region | Text | Sales region | Standardize labels |
| quantity | Numeric | Units sold | Non-negative unless returns exist |
| unit_price | Numeric | Selling price per unit | Validate currency/numeric type |
| revenue | Numeric | Sales revenue | Recalculate where possible |
| cost | Numeric | Transaction/product cost | Recalculate where possible |
| profit | Numeric | Revenue minus cost | revenue - cost |
| profit_margin | Numeric | Profit as a share of revenue | profit / revenue |

> Column names will be adjusted to match the selected dataset rather than forcing the data into this template.
