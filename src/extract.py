from pathlib import Path

import pandas as pd


RAW_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "candidates.csv"


def extract_candidates(source_path: Path = RAW_PATH) -> pd.DataFrame:
    """Read the semicolon-delimited source without applying business rules."""
    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")
    return pd.read_csv(source_path, sep=";", dtype={"Email": "string"})
