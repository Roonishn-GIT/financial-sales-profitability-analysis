"""Run exploratory analysis and create portfolio charts from cleaned data."""

from argparse import ArgumentParser
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, PercentFormatter
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "cleaned" / "financial_sales_cleaned.csv"
DEFAULT_VISUALS = PROJECT_ROOT / "visuals"

EXPECTED_CATEGORIES = {
    "Electronics": (57_485_698.06, 8_065_113.92, 14.03),
    "Home & Furniture": (47_674_426.96, 11_218_596.44, 23.53),
    "Clothing & Apparel": (27_134_365.30, 8_826_851.49, 32.53),
    "Accessories": (10_113_254.61, 3_438_046.28, 34.00),
}
EXPECTED_REGIONS = {
    "East": (44_980_048.22, 9_221_327.43, 20.50),
    "West": (36_242_841.73, 8_313_962.76, 22.94),
    "Central": (36_081_894.34, 8_094_863.77, 22.43),
    "South": (25_102_960.64, 5_918_454.17, 23.58),
}

BLUE = "#2F6690"
GREEN = "#3A7D44"
GOLD = "#D9A441"
RED = "#B44C43"
GRAY = "#667085"
CATEGORY_COLORS = {
    "Accessories": "#5B8E7D",
    "Clothing & Apparel": "#D9A441",
    "Electronics": "#B44C43",
    "Home & Furniture": "#2F6690",
}


def load_cleaned_data(path: str | Path) -> pd.DataFrame:
    """Load the validated cleaned CSV and parse its date column."""
    return pd.read_csv(path, parse_dates=["order_date"])


def safe_divide(numerator, denominator):
    """Divide while returning missing values when a denominator is zero."""
    if isinstance(denominator, pd.Series):
        denominator = denominator.where(denominator.ne(0))
    elif denominator == 0:
        denominator = float("nan")
    return numerator / denominator


def calculate_overall_kpis(df: pd.DataFrame) -> pd.Series:
    """Calculate company-level KPIs using weighted profit margin."""
    revenue = df["revenue"].sum()
    profit = df["profit"].sum()
    return pd.Series({
        "transaction_count": len(df),
        "units_sold": df["quantity"].sum(),
        "total_revenue": revenue,
        "total_profit": profit,
        "implied_cost": revenue - profit,
        "weighted_profit_margin": safe_divide(profit, revenue),
    })


def calculate_yearly_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize annual performance and year-over-year growth."""
    yearly = (
        df.assign(year=df["order_date"].dt.year)
        .groupby("year", as_index=False)
        .agg(
            transactions=("order_id", "size"), units=("quantity", "sum"),
            revenue=("revenue", "sum"), profit=("profit", "sum"),
        )
    )
    yearly["weighted_profit_margin"] = safe_divide(yearly["profit"], yearly["revenue"])
    yearly["yoy_revenue_growth"] = yearly["revenue"].pct_change()
    yearly["yoy_profit_growth"] = yearly["profit"].pct_change()
    return yearly


def calculate_category_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate category performance and company contribution shares."""
    category = (
        df.groupby("category", as_index=False)
        .agg(
            transactions=("order_id", "size"), units=("quantity", "sum"),
            revenue=("revenue", "sum"), profit=("profit", "sum"),
            implied_cost=("implied_cost", "sum"),
        )
        .sort_values("revenue", ascending=False).reset_index(drop=True)
    )
    category["weighted_profit_margin"] = safe_divide(category["profit"], category["revenue"])
    category["revenue_share"] = safe_divide(category["revenue"], category["revenue"].sum())
    category["profit_share"] = safe_divide(category["profit"], category["profit"].sum())
    return category


def calculate_regional_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate regional performance and revenue contribution."""
    region = (
        df.groupby("region", as_index=False)
        .agg(
            transactions=("order_id", "size"), units=("quantity", "sum"),
            revenue=("revenue", "sum"), profit=("profit", "sum"),
        )
        .sort_values("revenue", ascending=False).reset_index(drop=True)
    )
    region["weighted_profit_margin"] = safe_divide(region["profit"], region["revenue"])
    region["revenue_share"] = safe_divide(region["revenue"], region["revenue"].sum())
    return region


def calculate_customer_analysis(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, float]:
    """Aggregate source Customer_Name labels and return the top 10 by revenue."""
    customers = (
        df.groupby("customer_name", as_index=False)
        .agg(
            transactions=("order_id", "size"), revenue=("revenue", "sum"),
            profit=("profit", "sum"),
        )
        .sort_values(["revenue", "customer_name"], ascending=[False, True])
        .reset_index(drop=True)
    )
    customers["weighted_profit_margin"] = safe_divide(customers["profit"], customers["revenue"])
    top_10 = customers.head(10).copy()
    top_10_share = safe_divide(top_10["revenue"].sum(), customers["revenue"].sum())
    return customers, top_10, top_10_share


def calculate_monthly_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly performance and month-over-month revenue growth."""
    monthly = (
        df.assign(month=df["order_date"].dt.to_period("M").dt.to_timestamp())
        .groupby("month", as_index=False)
        .agg(
            transactions=("order_id", "size"), units=("quantity", "sum"),
            revenue=("revenue", "sum"), profit=("profit", "sum"),
        )
        .sort_values("month").reset_index(drop=True)
    )
    monthly["weighted_profit_margin"] = safe_divide(monthly["profit"], monthly["revenue"])
    monthly["mom_revenue_growth"] = monthly["revenue"].pct_change()
    return monthly


def calculate_product_margin_analysis(
    df: pd.DataFrame, company_margin: float
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Identify above-average-revenue products with below-company margin."""
    products = (
        df.groupby(["category", "sub_category", "product_name"], as_index=False)
        .agg(units=("quantity", "sum"), revenue=("revenue", "sum"), profit=("profit", "sum"))
    )
    products["weighted_profit_margin"] = safe_divide(products["profit"], products["revenue"])
    flagged = products.loc[
        products["revenue"].gt(products["revenue"].mean())
        & products["weighted_profit_margin"].lt(company_margin)
    ].sort_values("revenue", ascending=False).reset_index(drop=True)
    return products, flagged


def millions(value: float, _position: int) -> str:
    """Format an axis value as dollars in millions."""
    return f"${value / 1_000_000:.0f}M"


def thousands(value: float, _position: int) -> str:
    """Format an axis value as dollars in thousands."""
    return f"${value / 1_000:.0f}K"


def apply_chart_style(ax: plt.Axes) -> None:
    """Apply a consistent, simple visual style to a chart."""
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#D0D5DD", linewidth=0.7, alpha=0.65)
    ax.set_axisbelow(True)


def save_figure(fig: plt.Figure, path: Path) -> None:
    """Save a chart with consistent resolution and spacing."""
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def chart_category(category: pd.DataFrame, output_path: Path) -> None:
    """Create a grouped category revenue and profit chart."""
    plot_data = category.sort_values("revenue")
    fig, ax = plt.subplots(figsize=(10, 6))
    positions = list(range(len(plot_data)))
    ax.barh([y - 0.18 for y in positions], plot_data["revenue"], height=0.34, color=BLUE, label="Revenue")
    ax.barh([y + 0.18 for y in positions], plot_data["profit"], height=0.34, color=GREEN, label="Profit")
    ax.set_yticks(positions, plot_data["category"])
    ax.xaxis.set_major_formatter(FuncFormatter(millions))
    ax.set_xlabel("USD")
    ax.set_title("Revenue and Profit by Category", loc="left", fontsize=15, fontweight="bold")
    ax.legend(frameon=False, ncols=2, loc="lower right")
    apply_chart_style(ax)
    ax.grid(axis="x", color="#D0D5DD", linewidth=0.7, alpha=0.65)
    ax.grid(axis="y", visible=False)
    save_figure(fig, output_path)


def chart_monthly(monthly: pd.DataFrame, output_path: Path) -> None:
    """Create monthly revenue and profit trend lines."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly["month"], monthly["revenue"], color=BLUE, linewidth=2.4, marker="o", markersize=4, label="Revenue")
    ax.plot(monthly["month"], monthly["profit"], color=GREEN, linewidth=2.4, marker="o", markersize=4, label="Profit")
    ax.yaxis.set_major_formatter(FuncFormatter(millions))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
    ax.set_xlim(monthly["month"].min(), monthly["month"].max())
    ax.set_ylabel("USD")
    ax.set_title("Monthly Revenue and Profit Trend", loc="left", fontsize=15, fontweight="bold")
    ax.legend(frameon=False, ncols=2)
    apply_chart_style(ax)
    save_figure(fig, output_path)


def chart_regions(region: pd.DataFrame, output_path: Path) -> None:
    """Create a regional revenue and weighted-margin comparison."""
    plot_data = region.sort_values("revenue", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(plot_data["region"], plot_data["revenue"], color=BLUE, alpha=0.9, label="Revenue")
    ax.yaxis.set_major_formatter(FuncFormatter(millions))
    ax.set_ylabel("Revenue (USD)")
    ax.set_title("Regional Revenue and Profitability", loc="left", fontsize=15, fontweight="bold")
    apply_chart_style(ax)
    margin_ax = ax.twinx()
    margin_ax.plot(plot_data["region"], plot_data["weighted_profit_margin"], color=GOLD, marker="o", linewidth=2.5, label="Weighted margin")
    margin_ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    margin_ax.set_ylabel("Weighted profit margin")
    margin_ax.spines["top"].set_visible(False)
    margin_ax.set_ylim(0, max(plot_data["weighted_profit_margin"]) * 1.35)
    for bar, margin in zip(bars, plot_data["weighted_profit_margin"]):
        margin_ax.annotate(f"{margin:.1%}", (bar.get_x() + bar.get_width() / 2, margin), xytext=(0, 8), textcoords="offset points", ha="center", color="#7A5B00")
    handles_1, labels_1 = ax.get_legend_handles_labels()
    handles_2, labels_2 = margin_ax.get_legend_handles_labels()
    ax.legend(handles_1 + handles_2, labels_1 + labels_2, frameon=False, ncols=2, loc="upper right")
    save_figure(fig, output_path)


def chart_top_customers(top_10: pd.DataFrame, output_path: Path) -> None:
    """Create a horizontal bar chart for top Customer_Name labels."""
    plot_data = top_10.sort_values("revenue")
    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.barh(plot_data["customer_name"], plot_data["revenue"], color=BLUE)
    ax.xaxis.set_major_formatter(FuncFormatter(thousands))
    ax.set_xlabel("Revenue (USD)")
    ax.set_title("Top 10 Customer Names by Revenue", loc="left", fontsize=15, fontweight="bold", pad=28)
    ax.text(0, 1.01, "Customer_Name is a source label, not a unique customer ID.", transform=ax.transAxes, color=GRAY, fontsize=9)
    for bar, value in zip(bars, plot_data["revenue"]):
        ax.text(value, bar.get_y() + bar.get_height() / 2, f"  ${value / 1_000:,.0f}K", va="center", fontsize=9)
    apply_chart_style(ax)
    ax.grid(axis="x", color="#D0D5DD", linewidth=0.7, alpha=0.65)
    ax.grid(axis="y", visible=False)
    save_figure(fig, output_path)


def chart_margin_analysis(
    products: pd.DataFrame, flagged: pd.DataFrame, company_margin: float, output_path: Path
) -> None:
    """Plot product revenue against weighted margin and highlight risk products."""
    average_product_revenue = products["revenue"].mean()
    fig, ax = plt.subplots(figsize=(11, 7))
    for category, group in products.groupby("category"):
        ax.scatter(
            group["revenue"], group["weighted_profit_margin"], s=65, alpha=0.8,
            color=CATEGORY_COLORS.get(category, GRAY), label=category,
            edgecolor="white", linewidth=0.6,
        )
    ax.axhline(company_margin, color=RED, linestyle="--", linewidth=1.5, label=f"Company margin ({company_margin:.1%})")
    ax.axvline(average_product_revenue, color=GRAY, linestyle=":", linewidth=1.5, label="Average product revenue")
    label_offsets = [(10, 30), (-10, 50), (-10, 30), (-20, 50)]
    for row, offset in zip(flagged.head(4).itertuples(), label_offsets):
        ax.annotate(
            row.product_name, (row.revenue, row.weighted_profit_margin),
            xytext=offset, textcoords="offset points", ha="center", fontsize=8,
            arrowprops={"arrowstyle": "-", "color": GRAY, "linewidth": 0.7},
        )
    ax.xaxis.set_major_formatter(FuncFormatter(millions))
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    ax.set_xlabel("Product revenue (USD)")
    ax.set_ylabel("Weighted profit margin")
    ax.set_title("Product Revenue and Margin Analysis", loc="left", fontsize=15, fontweight="bold", pad=28)
    ax.text(0, 1.01, "Labels mark high-revenue products below the company margin.", transform=ax.transAxes, color=GRAY, fontsize=9)
    ax.legend(frameon=False, fontsize=8, ncols=2, loc="upper right")
    apply_chart_style(ax)
    save_figure(fig, output_path)


def reconcile_summary(
    name: str, key: str, actual: pd.DataFrame,
    expected: dict[str, tuple[float, float, float]],
) -> bool:
    """Reconcile grouped revenue, profit, and margin to expected SQL results."""
    print(f"\n{name} RECONCILIATION")
    passed_all = True
    indexed = actual.set_index(key)
    for label, (expected_revenue, expected_profit, expected_margin_pct) in expected.items():
        row = indexed.loc[label]
        passed = (
            round(row["revenue"], 2) == expected_revenue
            and round(row["profit"], 2) == expected_profit
            and round(row["weighted_profit_margin"] * 100, 2) == expected_margin_pct
        )
        print(
            f"{'PASS' if passed else 'FAIL'} | {label:<20} | "
            f"Revenue ${row['revenue']:,.2f} | Profit ${row['profit']:,.2f} | "
            f"Margin {row['weighted_profit_margin']:.2%}"
        )
        passed_all = passed_all and passed
    return passed_all


def print_results(
    overall: pd.Series, yearly: pd.DataFrame, category: pd.DataFrame,
    region: pd.DataFrame, top_10: pd.DataFrame, top_10_share: float,
    monthly: pd.DataFrame, flagged: pd.DataFrame,
) -> bool:
    """Print important analysis outputs and SQL reconciliation results."""
    print("\nOVERALL KPIs")
    print(f"Transactions: {overall['transaction_count']:,.0f}")
    print(f"Units sold: {overall['units_sold']:,.0f}")
    print(f"Revenue: ${overall['total_revenue']:,.2f}")
    print(f"Profit: ${overall['total_profit']:,.2f}")
    print(f"Implied cost: ${overall['implied_cost']:,.2f}")
    print(f"Weighted profit margin: {overall['weighted_profit_margin']:.2%}")

    print("\nYEARLY ANALYSIS")
    yearly_display = yearly.copy()
    for column in ["revenue", "profit"]:
        yearly_display[column] = yearly_display[column].map(lambda value: f"${value:,.2f}")
    for column in ["weighted_profit_margin", "yoy_revenue_growth", "yoy_profit_growth"]:
        yearly_display[column] = yearly_display[column].map(lambda value: "N/A" if pd.isna(value) else f"{value:.2%}")
    print(yearly_display.to_string(index=False))

    category_passed = reconcile_summary("CATEGORY", "category", category, EXPECTED_CATEGORIES)
    region_passed = reconcile_summary("REGIONAL", "region", region, EXPECTED_REGIONS)

    print("\nTOP 10 CUSTOMER_NAME LABELS BY REVENUE")
    customer_display = top_10[["customer_name", "transactions", "revenue", "profit"]].copy()
    customer_display["revenue"] = customer_display["revenue"].map(lambda value: f"${value:,.2f}")
    customer_display["profit"] = customer_display["profit"].map(lambda value: f"${value:,.2f}")
    print(customer_display.to_string(index=False))
    print(f"Top 10 share of company revenue: {top_10_share:.2%}")
    print("Note: Customer_Name is not a unique customer ID.")

    print("\nMONTHLY TREND SUMMARY")
    print(f"Months analyzed: {len(monthly)} ({monthly['month'].min():%Y-%m} through {monthly['month'].max():%Y-%m})")
    peak = monthly.loc[monthly["revenue"].idxmax()]
    trough = monthly.loc[monthly["revenue"].idxmin()]
    print(f"Highest-revenue month: {peak['month']:%Y-%m} (${peak['revenue']:,.2f})")
    print(f"Lowest-revenue month: {trough['month']:%Y-%m} (${trough['revenue']:,.2f})")

    print("\nHIGH-REVENUE PRODUCTS BELOW COMPANY MARGIN")
    flagged_display = flagged[["category", "product_name", "revenue", "profit", "weighted_profit_margin"]].copy()
    flagged_display["revenue"] = flagged_display["revenue"].map(lambda value: f"${value:,.2f}")
    flagged_display["profit"] = flagged_display["profit"].map(lambda value: f"${value:,.2f}")
    flagged_display["weighted_profit_margin"] = flagged_display["weighted_profit_margin"].map(lambda value: f"{value:.2%}")
    print(flagged_display.to_string(index=False))
    electronics_count = int(flagged["category"].eq("Electronics").sum())
    electronics_revenue_share = safe_divide(
        flagged.loc[flagged["category"].eq("Electronics"), "revenue"].sum(),
        flagged["revenue"].sum(),
    )
    print(
        f"Electronics accounts for {electronics_count} of {len(flagged)} flagged products "
        f"and {electronics_revenue_share:.2%} of flagged-product revenue."
    )
    return category_passed and region_passed


def build_parser() -> ArgumentParser:
    """Build command-line arguments for input and chart output paths."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--visuals-dir", type=Path, default=DEFAULT_VISUALS)
    return parser


def main() -> None:
    """Run the full Day 2 analysis, reconciliation, and chart workflow."""
    args = build_parser().parse_args()
    args.visuals_dir.mkdir(parents=True, exist_ok=True)
    df = load_cleaned_data(args.input)
    overall = calculate_overall_kpis(df)
    yearly = calculate_yearly_analysis(df)
    category = calculate_category_analysis(df)
    region = calculate_regional_analysis(df)
    _customers, top_10, top_10_share = calculate_customer_analysis(df)
    monthly = calculate_monthly_analysis(df)
    products, flagged = calculate_product_margin_analysis(df, overall["weighted_profit_margin"])
    reconciled = print_results(
        overall, yearly, category, region, top_10, top_10_share, monthly, flagged
    )
    chart_category(category, args.visuals_dir / "revenue_profit_by_category.png")
    chart_monthly(monthly, args.visuals_dir / "monthly_revenue_profit_trend.png")
    chart_regions(region, args.visuals_dir / "regional_profitability.png")
    chart_top_customers(top_10, args.visuals_dir / "top_customers.png")
    chart_margin_analysis(products, flagged, overall["weighted_profit_margin"], args.visuals_dir / "margin_analysis.png")
    print(f"\nSaved 5 charts to: {args.visuals_dir}")
    print("SQL RECONCILIATION:", "PASS" if reconciled else "FAIL")
    if not reconciled:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
