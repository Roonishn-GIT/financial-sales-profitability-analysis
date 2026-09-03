"""Reusable analysis helpers for Project 1."""

import pandas as pd


def summarize_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Return descriptive statistics for numeric columns."""
    return df.describe(include="number").T
