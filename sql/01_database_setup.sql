-- Project 1: Financial Sales & Profitability Analysis
-- 01_database_setup.sql
-- PostgreSQL schema setup for the validated 2023-2024 U.S. product sales dataset.
--
-- DESTRUCTIVE SETUP SCRIPT:
-- This file drops and recreates the project tables/view. Run it only when
-- intentionally rebuilding the database from scratch, BEFORE importing the CSV.
-- Do NOT rerun it after loading sales_stage unless you intend to delete/reload data.

DROP VIEW IF EXISTS sales_enriched;
DROP TABLE IF EXISTS sales_transactions;
DROP TABLE IF EXISTS sales_stage;

-- Staging table mirrors the raw CSV. Order date is loaded as text first
-- because the source uses MM-DD-YY formatting.
CREATE TABLE sales_stage (
    order_id        INTEGER,
    order_date      TEXT,
    customer_name   TEXT,
    city            TEXT,
    state           TEXT,
    region          TEXT,
    country         TEXT,
    category        TEXT,
    sub_category    TEXT,
    product_name    TEXT,
    quantity        INTEGER,
    unit_price      NUMERIC(12,2),
    revenue         NUMERIC(14,2),
    profit          NUMERIC(14,2)
);

-- Final typed transaction table.
CREATE TABLE sales_transactions (
    order_id        INTEGER PRIMARY KEY,
    order_date      DATE NOT NULL,
    customer_name   TEXT NOT NULL,
    city            TEXT NOT NULL,
    state           TEXT NOT NULL,
    region          TEXT NOT NULL,
    country         TEXT NOT NULL,
    category        TEXT NOT NULL,
    sub_category    TEXT NOT NULL,
    product_name    TEXT NOT NULL,
    quantity        INTEGER NOT NULL CHECK (quantity > 0),
    unit_price      NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
    revenue         NUMERIC(14,2) NOT NULL CHECK (revenue >= 0),
    profit          NUMERIC(14,2) NOT NULL
);

-- Reusable analytical view with derived KPIs and time dimensions.
CREATE VIEW sales_enriched AS
SELECT
    st.*,
    revenue - profit AS implied_cost,
    CASE WHEN revenue = 0 THEN 0 ELSE profit / revenue END AS profit_margin,
    CASE WHEN quantity = 0 THEN NULL ELSE revenue / quantity END AS revenue_per_unit,
    CASE WHEN quantity = 0 THEN NULL ELSE profit / quantity END AS profit_per_unit,
    EXTRACT(YEAR FROM order_date)::INTEGER AS year,
    EXTRACT(QUARTER FROM order_date)::INTEGER AS quarter,
    DATE_TRUNC('month', order_date)::DATE AS month
FROM sales_transactions st;

-- Helpful indexes for common portfolio analysis queries.
CREATE INDEX idx_sales_order_date ON sales_transactions(order_date);
CREATE INDEX idx_sales_category ON sales_transactions(category);
CREATE INDEX idx_sales_region ON sales_transactions(region);
CREATE INDEX idx_sales_state ON sales_transactions(state);
CREATE INDEX idx_sales_customer ON sales_transactions(customer_name);
