# Business Problem

## Business Context
A U.S. retailer has 200,000 transaction-level sales records covering January 2023 through December 2024. Leadership wants to understand whether revenue growth is translating into profitable growth, which products and customers create the most value, and where geographic performance or margin efficiency is lagging.

## Primary Objective
Identify the key drivers of revenue, implied cost, profit, and profit margin across products, customers, states, regions, and time, then translate the findings into practical recommendations for profitable growth.

## Primary Stakeholder
Executive, finance, and sales leadership responsible for revenue growth, product strategy, geographic performance, and profitability improvement.

## Core Business Questions
1. How did revenue, profit, implied cost, units, and margin change from 2023 to 2024?
2. Which categories, sub-categories, and products generate the most revenue and profit?
3. Which high-revenue products or markets have comparatively weak margins?
4. Which customers contribute the most revenue and profit, and how concentrated is customer value?
5. Which regions, states, and cities lead or lag on revenue, profit, and margin?
6. What monthly and quarterly trends, growth rates, and seasonality patterns are visible?
7. Where can management focus to improve profitability without sacrificing meaningful revenue?

## KPI Framework
- Total Revenue
- Implied Cost = Revenue - Profit
- Total Profit
- Profit Margin % = Profit / Revenue
- Orders
- Units Sold
- Average Order Value
- Revenue per Unit
- Profit per Unit
- Revenue Growth %
- Profit Growth %
- Revenue / Profit Contribution %

## Scope and Analytical Notes
- The dataset is synthetic U.S. retail transaction data covering 2023-2024.
- `Order_ID` is unique in the supplied data, so each row is treated as one transaction record.
- The dataset supplies Revenue and Profit but not a raw cost field. `Implied Cost` will therefore be derived as Revenue minus Profit and documented as a calculated measure rather than raw COGS.
- `Customer_Name` is the only customer-level identifier provided, so customer analysis will use the supplied name as the analytical customer key.
- The raw region value `Centre` corresponds to central/Midwestern U.S. states. Raw data will remain unchanged; the cleaned analytical field will standardize this label to `Central`.

## Success Criteria
The final project should produce reproducible calculations across Excel, PostgreSQL, Python, and Power BI; reconcile headline KPIs across tools; identify meaningful profitability patterns; and deliver an executive dashboard plus concise business recommendations.
