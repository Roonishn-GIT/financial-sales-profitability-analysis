"""Validate the cleaned dataset against the exact Day 1 controls."""

from argparse import ArgumentParser
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "cleaned" / "financial_sales_cleaned.csv"
REQUIRED_FIELDS = [
    "order_id", "order_date", "customer_name", "city", "state", "region",
    "country", "category", "sub_category", "product_name", "quantity",
    "unit_price", "revenue", "profit",
]
EXPECTED_REGIONS = {"Central", "East", "South", "West"}
DERIVED_FIELDS = ["implied_cost", "profit_margin", "revenue_per_unit", "profit_per_unit"]


def report(name: str, actual: object, expected: object, passed: bool) -> bool:
    """Print one readable validation result and return its status."""
    status = "PASS" if passed else "FAIL"
    print(f"{status:<4} | {name:<32} | actual: {actual} | expected: {expected}")
    return passed


def validate(df: pd.DataFrame) -> bool:
    """Run all Day 1 reconciliation and cleaned-data quality checks."""
    results: list[bool] = []
    missing_columns = sorted(set(REQUIRED_FIELDS + DERIVED_FIELDS).difference(df.columns))
    results.append(report("Required columns present", missing_columns, "none missing", not missing_columns))
    if missing_columns:
        return False

    df["order_date"] = pd.to_datetime(df["order_date"], errors="raise")
    row_count = len(df)
    unique_orders = df["order_id"].nunique(dropna=True)
    duplicate_order_ids = int(df["order_id"].duplicated().sum())
    total_units = int(df["quantity"].sum())
    total_revenue = round(float(df["revenue"].sum()), 2)
    total_profit = round(float(df["profit"].sum()), 2)
    implied_cost = round(float((df["revenue"] - df["profit"]).sum()), 2)
    weighted_margin = round(total_profit / total_revenue * 100, 2)

    results.extend([
        report("Row count", row_count, 200000, row_count == 200000),
        report("Unique Order IDs", unique_orders, 200000, unique_orders == 200000),
        report("Duplicate Order IDs", duplicate_order_ids, 0, duplicate_order_ids == 0),
        report("Total Units", total_units, 370800, total_units == 370800),
        report("Total Revenue", f"{total_revenue:.2f}", "142407744.93", total_revenue == 142407744.93),
        report("Total Profit", f"{total_profit:.2f}", "31548608.13", total_profit == 31548608.13),
        report("Implied Cost", f"{implied_cost:.2f}", "110859136.80", implied_cost == 110859136.80),
        report("Weighted Profit Margin", f"{weighted_margin:.2f}%", "22.15%", weighted_margin == 22.15),
        report("Minimum Date", df["order_date"].min().date(), "2023-01-01", str(df["order_date"].min().date()) == "2023-01-01"),
        report("Maximum Date", df["order_date"].max().date(), "2024-12-31", str(df["order_date"].max().date()) == "2024-12-31"),
    ])

    # Day 1 defines an exception as a difference of at least two cents.
    revenue_difference = (df["revenue"] - df["quantity"] * df["unit_price"]).abs()
    revenue_exceptions = int(revenue_difference.ge(0.02).sum())
    results.append(report("Revenue formula exceptions", revenue_exceptions, 0, revenue_exceptions == 0))

    missing_required = int(df[REQUIRED_FIELDS].isna().sum().sum())
    text_fields = [column for column in REQUIRED_FIELDS if not pd.api.types.is_numeric_dtype(df[column])]
    blank_text = int(sum(df[column].astype("string").str.strip().eq("").sum() for column in text_fields))
    results.append(report("Missing required values", missing_required + blank_text, 0, missing_required + blank_text == 0))

    nonnumeric_derived = [column for column in DERIVED_FIELDS if not pd.api.types.is_numeric_dtype(df[column])]
    results.append(report("Derived fields are numeric", nonnumeric_derived, "all numeric", not nonnumeric_derived))
    infinite_derived = int(df[DERIVED_FIELDS].isin([float("inf"), float("-inf")]).sum().sum())
    results.append(report("Infinite derived values", infinite_derived, 0, infinite_derived == 0))
    duplicate_rows = int(df.duplicated().sum())
    results.append(report("Duplicate rows", duplicate_rows, 0, duplicate_rows == 0))
    actual_regions = set(df["region"].dropna().unique())
    results.append(report("Regions", sorted(actual_regions), sorted(EXPECTED_REGIONS), actual_regions == EXPECTED_REGIONS))
    countries = set(df["country"].dropna().unique())
    results.append(report("Country", sorted(countries), ["United States"], countries == {"United States"}))

    print("-" * 96)
    print("OVERALL RESULT:", "PASS" if all(results) else "FAIL")
    return all(results)


def build_parser() -> ArgumentParser:
    """Build the command-line argument parser."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    return parser


def main() -> None:
    """Load the cleaned CSV and exit nonzero if any validation fails."""
    args = build_parser().parse_args()
    cleaned = pd.read_csv(args.input)
    if not validate(cleaned):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
