"""Clean the raw financial sales CSV and create an analysis-ready dataset."""

from argparse import ArgumentParser
from pathlib import Path
import re

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "raw" / "product_sales_dataset_final.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "cleaned" / "financial_sales_cleaned.csv"
NUMERIC_COLUMNS = ["order_id", "quantity", "unit_price", "revenue", "profit"]


def load_data(path: str | Path) -> pd.DataFrame:
    """Load the raw CSV dataset without changing the source file."""
    return pd.read_csv(path)


def to_snake_case(column_name: str) -> str:
    """Convert a column label to lowercase snake_case."""
    cleaned_name = column_name.strip().lower()
    return re.sub(r"[^a-z0-9]+", "_", cleaned_name).strip("_")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the documented Day 2 cleaning and derived-field rules."""
    cleaned = df.copy()
    cleaned.columns = [to_snake_case(column) for column in cleaned.columns]

    required_columns = {
        "order_id", "order_date", "region", "quantity", "unit_price", "revenue", "profit"
    }
    missing_columns = required_columns.difference(cleaned.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    # errors="raise" makes malformed dates and non-numeric values immediately visible.
    cleaned["order_date"] = pd.to_datetime(
        cleaned["order_date"], format="%m-%d-%y", errors="raise"
    )
    cleaned["region"] = cleaned["region"].replace({"Centre": "Central"})

    for column in NUMERIC_COLUMNS:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="raise")

    # Currency-derived columns are rounded to cents for a clean CSV export.
    cleaned["implied_cost"] = (cleaned["revenue"] - cleaned["profit"]).round(2)

    # A zero denominator produces a missing value instead of infinity or an error.
    cleaned["profit_margin"] = cleaned["profit"].div(
        cleaned["revenue"].where(cleaned["revenue"].ne(0))
    )
    nonzero_quantity = cleaned["quantity"].where(cleaned["quantity"].ne(0))
    cleaned["revenue_per_unit"] = cleaned["revenue"].div(nonzero_quantity).round(2)
    cleaned["profit_per_unit"] = cleaned["profit"].div(nonzero_quantity).round(2)
    return cleaned


def save_cleaned_data(df: pd.DataFrame, path: str | Path) -> None:
    """Write cleaned data to a new CSV, creating its directory if needed."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, date_format="%Y-%m-%d")


def build_parser() -> ArgumentParser:
    """Build the command-line argument parser."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser


def main() -> None:
    """Load, clean, and save the dataset."""
    args = build_parser().parse_args()
    cleaned = clean_data(load_data(args.input))
    save_cleaned_data(cleaned, args.output)
    print(f"Cleaned {len(cleaned):,} rows.")
    print(f"Saved cleaned data to: {args.output}")


if __name__ == "__main__":
    main()
