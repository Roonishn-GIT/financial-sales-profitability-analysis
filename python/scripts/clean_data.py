"""Data-cleaning utilities for the financial sales profitability project."""

import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    """Load the raw CSV dataset."""
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply documented cleaning rules after the source schema is validated."""
    cleaned = df.copy()
    cleaned.columns = (
        cleaned.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
    )
    return cleaned
