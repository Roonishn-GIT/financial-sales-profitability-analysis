-- Project 1: Financial Sales & Profitability Analysis
-- 06_trend_analysis.sql
-- Monthly trends, growth, running totals, rolling averages, regional performance, and seasonality.

-- 1) Monthly revenue, profit, units, and margin
SELECT
    DATE_TRUNC('month', order_date)::DATE AS month,
    COUNT(*) AS transactions,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue), 0), 2) AS profit_margin_pct
FROM sales_transactions
GROUP BY 1
ORDER BY 1;

-- 2) Month-over-month growth using LAG()
WITH monthly_kpis AS (
    SELECT
        DATE_TRUNC('month', order_date)::DATE AS month,
        SUM(revenue) AS revenue,
        SUM(profit) AS profit,
        SUM(quantity) AS units_sold
    FROM sales_transactions
    GROUP BY 1
),
monthly_with_prior AS (
    SELECT
        month,
        revenue,
        profit,
        units_sold,
        LAG(revenue) OVER (ORDER BY month) AS prior_revenue,
        LAG(profit) OVER (ORDER BY month) AS prior_profit,
        LAG(units_sold) OVER (ORDER BY month) AS prior_units
    FROM monthly_kpis
)
SELECT
    month,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,
    units_sold,
    ROUND(100.0 * (revenue - prior_revenue) / NULLIF(prior_revenue, 0), 2) AS revenue_mom_growth_pct,
    ROUND(100.0 * (profit - prior_profit) / NULLIF(prior_profit, 0), 2) AS profit_mom_growth_pct,
    ROUND(100.0 * (units_sold - prior_units) / NULLIF(prior_units, 0), 2) AS units_mom_growth_pct
FROM monthly_with_prior
ORDER BY month;

-- 3) Running revenue and profit totals
WITH monthly_kpis AS (
    SELECT
        DATE_TRUNC('month', order_date)::DATE AS month,
        SUM(revenue) AS revenue,
        SUM(profit) AS profit
    FROM sales_transactions
    GROUP BY 1
)
SELECT
    month,
    ROUND(revenue, 2) AS monthly_revenue,
    ROUND(profit, 2) AS monthly_profit,
    ROUND(SUM(revenue) OVER (ORDER BY month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_revenue,
    ROUND(SUM(profit) OVER (ORDER BY month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_profit
FROM monthly_kpis
ORDER BY month;

-- 4) Three-month rolling averages to smooth short-term volatility
WITH monthly_kpis AS (
    SELECT
        DATE_TRUNC('month', order_date)::DATE AS month,
        SUM(revenue) AS revenue,
        SUM(profit) AS profit
    FROM sales_transactions
    GROUP BY 1
)
SELECT
    month,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,
    ROUND(AVG(revenue) OVER (
        ORDER BY month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS revenue_3mo_moving_avg,
    ROUND(AVG(profit) OVER (
        ORDER BY month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS profit_3mo_moving_avg
FROM monthly_kpis
ORDER BY month;

-- 5) Regional performance, contribution, and rankings
WITH region_kpis AS (
    SELECT
        region,
        COUNT(*) AS transactions,
        SUM(quantity) AS units_sold,
        SUM(revenue) AS revenue,
        SUM(profit) AS profit
    FROM sales_transactions
    GROUP BY region
)
SELECT
    region,
    transactions,
    units_sold,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,
    ROUND(100.0 * profit / NULLIF(revenue, 0), 2) AS profit_margin_pct,
    ROUND(100.0 * revenue / NULLIF(SUM(revenue) OVER (), 0), 2) AS revenue_share_pct,
    ROUND(100.0 * profit / NULLIF(SUM(profit) OVER (), 0), 2) AS profit_share_pct,
    RANK() OVER (ORDER BY revenue DESC) AS revenue_rank,
    RANK() OVER (ORDER BY profit DESC) AS profit_rank,
    RANK() OVER (ORDER BY (profit / NULLIF(revenue, 0)) DESC) AS margin_rank
FROM region_kpis
ORDER BY revenue_rank;

-- 6) Seasonality by calendar month across 2023-2024
SELECT
    EXTRACT(MONTH FROM order_date)::INTEGER AS month_number,
    TO_CHAR(order_date, 'Mon') AS month_name,
    ROUND(AVG(revenue), 2) AS avg_transaction_revenue,
    ROUND(AVG(profit), 2) AS avg_transaction_profit,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue), 0), 2) AS profit_margin_pct
FROM sales_transactions
GROUP BY 1, 2
ORDER BY 1;
