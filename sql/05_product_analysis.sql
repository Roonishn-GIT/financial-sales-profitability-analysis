-- Project 1: Financial Sales & Profitability Analysis
-- 05_product_analysis.sql
-- Product, sub-category, and category profitability analysis.

-- 1) Category-level KPI summary
SELECT
    category,
    COUNT(*) AS transactions,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(SUM(revenue - profit), 2) AS implied_cost,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue), 0), 2) AS profit_margin_pct
FROM sales_transactions
GROUP BY category
ORDER BY revenue DESC;

-- 2) Category contribution to total company revenue and profit
-- Demonstrates aggregate window functions.
SELECT
    category,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(100.0 * SUM(revenue) / NULLIF(SUM(SUM(revenue)) OVER (), 0), 2) AS revenue_share_pct,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(SUM(profit)) OVER (), 0), 2) AS profit_share_pct,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue), 0), 2) AS profit_margin_pct
FROM sales_transactions
GROUP BY category
ORDER BY revenue DESC;

-- 3) Product rankings by revenue and profit
WITH product_kpis AS (
    SELECT
        category,
        sub_category,
        product_name,
        SUM(quantity) AS units_sold,
        SUM(revenue) AS revenue,
        SUM(profit) AS profit
    FROM sales_transactions
    GROUP BY category, sub_category, product_name
), ranked AS (
    SELECT
        category,
        sub_category,
        product_name,
        units_sold,
        revenue,
        profit,
        RANK() OVER (ORDER BY revenue DESC) AS revenue_rank,
        DENSE_RANK() OVER (ORDER BY profit DESC) AS profit_rank
    FROM product_kpis
)
SELECT
    category,
    sub_category,
    product_name,
    units_sold,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,
    ROUND(100.0 * profit / NULLIF(revenue, 0), 2) AS profit_margin_pct,
    revenue_rank,
    profit_rank
FROM ranked
ORDER BY revenue_rank
LIMIT 20;

-- 4) High-revenue, below-average-margin products
-- Flags products that sell strongly but convert revenue to profit inefficiently.
WITH product_kpis AS (
    SELECT
        category,
        sub_category,
        product_name,
        SUM(revenue) AS revenue,
        SUM(profit) AS profit
    FROM sales_transactions
    GROUP BY category, sub_category, product_name
), benchmarks AS (
    SELECT
        AVG(revenue) AS avg_product_revenue,
        SUM(profit) / NULLIF(SUM(revenue), 0) AS overall_margin
    FROM product_kpis
)
SELECT
    p.category,
    p.sub_category,
    p.product_name,
    ROUND(p.revenue, 2) AS revenue,
    ROUND(p.profit, 2) AS profit,
    ROUND(100.0 * p.profit / NULLIF(p.revenue, 0), 2) AS profit_margin_pct
FROM product_kpis p
CROSS JOIN benchmarks b
WHERE p.revenue > b.avg_product_revenue
  AND p.profit / NULLIF(p.revenue, 0) < b.overall_margin
ORDER BY p.revenue DESC;

-- 5) Sub-category performance and ranking within each category
WITH subcategory_kpis AS (
    SELECT
        category,
        sub_category,
        SUM(quantity) AS units_sold,
        SUM(revenue) AS revenue,
        SUM(profit) AS profit
    FROM sales_transactions
    GROUP BY category, sub_category
)
SELECT
    category,
    sub_category,
    units_sold,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,
    ROUND(100.0 * profit / NULLIF(revenue, 0), 2) AS profit_margin_pct,
    RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS revenue_rank_within_category,
    RANK() OVER (PARTITION BY category ORDER BY profit DESC) AS profit_rank_within_category
FROM subcategory_kpis
ORDER BY category, revenue_rank_within_category, sub_category;
