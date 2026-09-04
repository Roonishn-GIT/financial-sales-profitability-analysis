-- Project 1: Financial Sales & Profitability Analysis
-- 04_customer_analysis.sql
-- Customer-level performance, ranking, and concentration analysis.

-- 1) Customer performance summary
SELECT
    customer_name,
    COUNT(*) AS transactions,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue), 0), 2) AS profit_margin_pct,
    ROUND(SUM(revenue) / COUNT(*), 2) AS avg_transaction_value
FROM sales_transactions
GROUP BY customer_name
ORDER BY revenue DESC;

-- 2) Revenue and profit rankings using window functions
WITH customer_kpis AS (
    SELECT
        customer_name,
        COUNT(*) AS transactions,
        SUM(quantity) AS units_sold,
        SUM(revenue) AS revenue,
        SUM(profit) AS profit
    FROM sales_transactions
    GROUP BY customer_name
)
SELECT
    customer_name,
    transactions,
    units_sold,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,
    ROUND(100.0 * profit / NULLIF(revenue, 0), 2) AS profit_margin_pct,
    RANK() OVER (ORDER BY revenue DESC) AS revenue_rank,
    DENSE_RANK() OVER (ORDER BY profit DESC) AS profit_rank
FROM customer_kpis
ORDER BY revenue_rank, customer_name;

-- 3) Top 10 customers by revenue
WITH customer_kpis AS (
    SELECT
        customer_name,
        SUM(revenue) AS revenue,
        SUM(profit) AS profit
    FROM sales_transactions
    GROUP BY customer_name
)
SELECT
    customer_name,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,
    ROUND(100.0 * profit / NULLIF(revenue, 0), 2) AS profit_margin_pct
FROM customer_kpis
ORDER BY revenue DESC
LIMIT 10;

-- 4) Top-10 customer concentration as a share of total company revenue/profit
WITH customer_kpis AS (
    SELECT
        customer_name,
        SUM(revenue) AS revenue,
        SUM(profit) AS profit
    FROM sales_transactions
    GROUP BY customer_name
),
ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (ORDER BY revenue DESC) AS revenue_row_num
    FROM customer_kpis
)
SELECT
    ROUND(SUM(CASE WHEN revenue_row_num <= 10 THEN revenue ELSE 0 END), 2) AS top_10_revenue,
    ROUND(100.0 * SUM(CASE WHEN revenue_row_num <= 10 THEN revenue ELSE 0 END)
          / NULLIF(SUM(revenue), 0), 2) AS top_10_revenue_share_pct,
    ROUND(SUM(CASE WHEN revenue_row_num <= 10 THEN profit ELSE 0 END), 2) AS top_10_profit,
    ROUND(100.0 * SUM(CASE WHEN revenue_row_num <= 10 THEN profit ELSE 0 END)
          / NULLIF(SUM(profit), 0), 2) AS top_10_profit_share_pct
FROM ranked;

-- 5) Customers where revenue rank and profit rank differ the most
WITH customer_kpis AS (
    SELECT
        customer_name,
        SUM(revenue) AS revenue,
        SUM(profit) AS profit
    FROM sales_transactions
    GROUP BY customer_name
),
ranked AS (
    SELECT
        customer_name,
        revenue,
        profit,
        RANK() OVER (ORDER BY revenue DESC) AS revenue_rank,
        RANK() OVER (ORDER BY profit DESC) AS profit_rank
    FROM customer_kpis
)
SELECT
    customer_name,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,
    revenue_rank,
    profit_rank,
    ABS(revenue_rank - profit_rank) AS rank_gap
FROM ranked
ORDER BY rank_gap DESC, revenue DESC
LIMIT 15;
