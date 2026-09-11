import pandas as pd


REQUIRED_COLUMNS = {
    "First Name", "Last Name", "Email", "Application Date", "Country", "YOE",
    "Seniority", "Technology", "Code Challenge Score", "Technical Interview Score",
}


def prepare_candidates(raw: pd.DataFrame) -> pd.DataFrame:
    """Perform only preparation required for the dimensional model."""
    missing_columns = REQUIRED_COLUMNS.difference(raw.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    df = raw.copy().drop_duplicates().reset_index(drop=True)
    df["Application Date"] = pd.to_datetime(df["Application Date"], errors="coerce")
    for column in ["YOE", "Code Challenge Score", "Technical Interview Score"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    for column in ["Country", "Seniority", "Technology"]:
        df[column] = df[column].astype("string").str.strip()

    required_for_model = [
        "Application Date", "Country", "YOE", "Seniority", "Technology",
        "Code Challenge Score", "Technical Interview Score",
    ]
    if df[required_for_model].isna().any().any():
        raise ValueError("Null values found in fields required by the dimensional model.")
    if not df["Code Challenge Score"].between(0, 10).all() or not df["Technical Interview Score"].between(0, 10).all():
        raise ValueError("Assessment scores must be between 0 and 10.")
    if (df["YOE"] < 0).any():
        raise ValueError("Years of experience cannot be negative.")
    return df


def apply_business_rules(prepared: pd.DataFrame) -> pd.DataFrame:
    """Apply the mandatory hiring rule before the data warehouse load."""
    df = prepared.copy()
    df["hired_flag"] = (
        (df["Code Challenge Score"] >= 7)
        & (df["Technical Interview Score"] >= 7)
    ).astype("int8")
    df["experience_band"] = pd.cut(
        df["YOE"], bins=[-1, 2, 5, 10, 20, float("inf")],
        labels=["0-2 years", "3-5 years", "6-10 years", "11-20 years", "21+ years"],
    ).astype("string")
    return df
