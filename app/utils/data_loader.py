from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.utils.dataset_schema import DATASET_COLUMNS, DATASET_DTYPES

DEFAULT_DATASET_PATH = Path(__file__).resolve().parents[2] / "data" / "wod_dataset.csv"


def _empty_dataset() -> pd.DataFrame:
    """Return an empty DataFrame with the expected MVP schema."""
    empty_df = pd.DataFrame(columns=DATASET_COLUMNS)
    return empty_df.astype(DATASET_DTYPES)


def load_wod_dataset(path: str | Path | None = None) -> pd.DataFrame:
    """Load the local WOD dataset for browsing/filtering and future programming.

    If the file is missing or invalid, returns an empty DataFrame with the expected schema.
    """
    dataset_path = Path(path) if path is not None else DEFAULT_DATASET_PATH

    if not dataset_path.exists():
        return _empty_dataset()

    try:
        df = pd.read_csv(dataset_path)
    except (OSError, pd.errors.ParserError, UnicodeDecodeError):
        return _empty_dataset()

    for col in DATASET_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    df = df[DATASET_COLUMNS].copy()

    try:
        df = df.astype(DATASET_DTYPES)
    except (TypeError, ValueError):
        return _empty_dataset()

    return df
