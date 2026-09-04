# Executive Summary

## Business Question

How can management grow revenue while protecting or improving profitability across products, customers, regions, and time?

## Validated KPIs

The Day 1 Excel/PostgreSQL analyses and Day 2 Python workflow reconcile to the same company-level controls:

- **200,000** unique transactions/orders
- **370,800** units sold
- **$142.41M** revenue
- **$110.86M** implied cost
- **$31.55M** profit
- **22.15%** weighted profit margin
- Coverage from **2023-01-01 through 2024-12-31**

## Most Important Findings

1. **Growth is positive but modest.** From 2023 to 2024, revenue increased **1.27%** and profit increased **1.22%**. Transaction growth was only **0.39%**, while units grew **0.86%**.
2. **Electronics is the largest revenue category but the weakest-margin category.** It generated **$57.49M** of revenue, or about **40.37%** of company revenue, but only a **14.03%** margin.
3. **Home & Furniture generates the most profit.** It produced **$11.22M** of profit with a **23.53%** margin.
4. **Accessories and Clothing & Apparel are margin leaders.** Their category margins are approximately **34.00%** and **32.53%**, respectively.
5. **Regional leadership is split.** East leads revenue at **$44.98M**, while South has the strongest regional margin at **23.58%**.
6. **High revenue does not always equal high profitability.** Customer revenue and profit ranks can diverge materially, reinforcing the need to evaluate customer value on both dimensions.

## Preliminary Recommendations

- Review Electronics pricing, sourcing, discounting, and product mix because the low margin appears across several major high-revenue products rather than one isolated SKU.
- Protect Home & Furniture as a major profit engine and investigate which sub-categories can support additional profitable growth.
- Compare the South region's higher-margin mix with the East region's higher-revenue mix to identify transferable commercial practices.
- Segment customers using both revenue and profit contribution rather than sales volume alone.
- Use the planned Power BI dashboard to monitor revenue scale, profit contribution, margin efficiency, and product-mix opportunities interactively.

## Status

Day 2 is complete and validated. Python independently reproduced the core controls and category/regional findings, then strengthened the product-margin analysis by confirming that high-revenue products below the company margin are concentrated in Electronics. The Power BI dashboard remains planned for Day 3.
