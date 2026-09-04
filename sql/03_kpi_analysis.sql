-- Project 1: Financial Sales & Profitability Analysis
-- 03_kpi_analysis.sql
-- Executive KPI calculations and year-over-year performance analysis.

-- 1) Overall executive KPIs
SELECT
    COUNT(*) AS transaction_count,
    COUNT(DISTINCT order_id) AS unique_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(revenue - profit), 2) AS implied_cost,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue), 0), 2) AS profit_margin_pct,
    ROUND(AVG(revenue), 2) AS avg_transaction_value,
    ROUND(AVG(profit), 2) AS avg_profit_per_transaction,
    ROUND(SUM(revenue) / NULLIF(SUM(quantity), 0), 2) AS revenue_per_unit,
    ROUND(SUM(profit) / NULLIF(SUM(quantity), 0), 2) AS profit_per_unit
FROM sales_transactions;

-- 2) Annual performance summary
SELECT
    EXTRACT(YEAR FROM order_date)::INTEGER AS year,
    COUNT(*) AS transactions,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(revenue - profit), 2) AS implied_cost,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue), 0), 2) AS profit_margin_pct,
    ROUND(AVG(revenue), 2) AS avg_transaction_value
FROM sales_transactions
GROUP BY 1
ORDER BY 1;

-- 3) Year-over-year growth using a CTE + LAG window function
WITH annual_kpis AS (
    SELECT
        EXTRACT(YEAR FROM order_date)::INTEGER AS year,
        COUNT(*) AS transactions,
        SUM(quantity) AS units_sold,
        SUM(revenue) AS revenue,
        SUM(profit) AS profit
    FROM sales_transactions
    GROUP BY 1
),
annual_with_prior AS (
    SELECT
        *,
        LAG(transactions) OVER (ORDER BY year) AS prior_transactions,
        LAG(units_sold) OVER (ORDER BY year) AS prior_units,
        LAG(revenue) OVER (ORDER BY year) AS prior_revenue,
        LAG(profit) OVER (ORDER BY year) AS prior_profit
    FROM annual_kpis
)
SELECT
    year,
    transactions,
    units_sold,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,
    ROUND(100.0 * profit / NULLIF(revenue, 0), 2) AS profit_margin_pct,
    ROUND(100.0 * (transactions - prior_transactions) / NULLIF(prior_transactions, 0), 2) AS transaction_growth_pct,
    ROUND(100.0 * (units_sold - prior_units) / NULLIF(prior_units, 0), 2) AS units_growth_pct,
    ROUND(100.0 * (revenue - prior_revenue) / NULLIF(prior_revenue, 0), 2) AS revenue_growth_pct,
    ROUND(100.0 * (profit - prior_profit) / NULLIF(prior_profit, 0), 2) AS profit_growth_pct
FROM annual_with_prior
ORDER BY year;

-- 4) Revenue and profit efficiency by year
SELECT
    EXTRACT(YEAR FROM order_date)::INTEGER AS year,
    ROUND(SUM(revenue) / NULLIF(SUM(quantity), 0), 2) AS revenue_per_unit,
    ROUND(SUM(profit) / NULLIF(SUM(quantity), 0), 2) AS profit_per_unit,
    ROUND(SUM(revenue - profit) / NULLIF(SUM(quantity), 0), 2) AS implied_cost_per_unit
FROM sales_transactions
GROUP BY 1
ORDER BY 1;
