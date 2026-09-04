-- Project 1: Financial Sales & Profitability Analysis
-- 01b_data_load.sql
-- Run AFTER importing product_sales_dataset_final.csv into sales_stage.
--
-- Expected staging count: 200,000 rows.
-- Run this load once per fresh database build. Because order_id is the primary key,
-- rerunning the INSERT after a successful load will correctly raise duplicate-key errors.

-- Safety check: staging table should contain 200,000 rows before the INSERT.
SELECT COUNT(*) AS staging_row_count
FROM sales_stage;

-- Transform raw staging data into the typed analytical table.
INSERT INTO sales_transactions (
    order_id,
    order_date,
    customer_name,
    city,
    state,
    region,
    country,
    category,
    sub_category,
    product_name,
    quantity,
    unit_price,
    revenue,
    profit
)
SELECT
    order_id,
    TO_DATE(order_date, 'MM-DD-YY'),
    TRIM(customer_name),
    TRIM(city),
    TRIM(state),
    CASE WHEN TRIM(region) = 'Centre' THEN 'Central' ELSE TRIM(region) END,
    TRIM(country),
    TRIM(category),
    TRIM(sub_category),
    TRIM(product_name),
    quantity,
    unit_price,
    revenue,
    profit
FROM sales_stage;

-- Final load check: should also equal 200,000 rows.
SELECT COUNT(*) AS final_row_count
FROM sales_transactions;
