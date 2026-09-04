-- Project 1: Financial Sales & Profitability Analysis
-- 02_data_validation.sql
-- Reconcile PostgreSQL results to the Excel validation controls.

-- 1) Row count: expected 200,000
SELECT COUNT(*) AS row_count
FROM sales_transactions;

-- 2) Unique orders and duplicates: expected 200,000 unique, 0 duplicates
SELECT
    COUNT(*) AS row_count,
    COUNT(DISTINCT order_id) AS unique_orders,
    COUNT(*) - COUNT(DISTINCT order_id) AS duplicate_order_ids
FROM sales_transactions;

-- 3) Core financial controls
-- Expected approximately:
-- revenue = 142,407,744.93
-- profit = 31,548,608.13
-- implied_cost = 110,859,136.80
-- weighted_profit_margin = 22.15%
-- units = 370,800
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(revenue - profit), 2) AS implied_cost,
    ROUND((SUM(profit) / NULLIF(SUM(revenue), 0)) * 100, 2) AS weighted_profit_margin_pct,
    SUM(quantity) AS total_units
FROM sales_transactions;

-- 4) Date range: expected 2023-01-01 through 2024-12-31
SELECT
    MIN(order_date) AS min_order_date,
    MAX(order_date) AS max_order_date
FROM sales_transactions;

-- 5) Revenue formula exceptions: expected 0
SELECT COUNT(*) AS revenue_formula_exceptions
FROM sales_transactions
WHERE ABS(revenue - (quantity * unit_price)) >= 0.02;

-- 6) Missing values in required columns: all expected 0
SELECT
    COUNT(*) FILTER (WHERE order_id IS NULL) AS missing_order_id,
    COUNT(*) FILTER (WHERE order_date IS NULL) AS missing_order_date,
    COUNT(*) FILTER (WHERE customer_name IS NULL OR BTRIM(customer_name) = '') AS missing_customer,
    COUNT(*) FILTER (WHERE product_name IS NULL OR BTRIM(product_name) = '') AS missing_product,
    COUNT(*) FILTER (WHERE region IS NULL OR BTRIM(region) = '') AS missing_region,
    COUNT(*) FILTER (WHERE quantity IS NULL) AS missing_quantity,
    COUNT(*) FILTER (WHERE unit_price IS NULL) AS missing_unit_price,
    COUNT(*) FILTER (WHERE revenue IS NULL) AS missing_revenue,
    COUNT(*) FILTER (WHERE profit IS NULL) AS missing_profit
FROM sales_transactions;

-- 7) Confirm region cleanup. Expected regions: Central, East, South, West.
SELECT region, COUNT(*) AS transactions
FROM sales_transactions
GROUP BY region
ORDER BY region;

-- 8) Basic financial range checks
SELECT
    MIN(quantity) AS min_quantity,
    MAX(quantity) AS max_quantity,
    MIN(unit_price) AS min_unit_price,
    MAX(unit_price) AS max_unit_price,
    MIN(revenue) AS min_revenue,
    MAX(revenue) AS max_revenue,
    MIN(profit) AS min_profit,
    MAX(profit) AS max_profit
FROM sales_transactions;
