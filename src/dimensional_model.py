import pandas as pd


def _surrogate_dimension(source: pd.DataFrame, columns: list[str], key_name: str) -> pd.DataFrame:
    dimension = source[columns].drop_duplicates().sort_values(columns).reset_index(drop=True)
    dimension.insert(0, key_name, range(1, len(dimension) + 1))
    return dimension


def build_dimensional_model(transformed: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Create dimensions, surrogate keys, mappings, and a fact table at application grain."""
    dim_date = _surrogate_dimension(transformed, ["Application Date"], "date_key")
    dim_date = dim_date.rename(columns={"Application Date": "full_date"})
    dim_date["year"] = dim_date["full_date"].dt.year
    dim_date["quarter"] = dim_date["full_date"].dt.quarter
    dim_date["month_number"] = dim_date["full_date"].dt.month
    dim_date["month_name"] = dim_date["full_date"].dt.month_name()

    dim_country = _surrogate_dimension(transformed, ["Country"], "country_key").rename(columns={"Country": "country"})
    dim_technology = _surrogate_dimension(transformed, ["Technology"], "technology_key").rename(columns={"Technology": "technology"})
    dim_candidate_profile = _surrogate_dimension(
        transformed, ["Seniority", "YOE", "experience_band"], "candidate_profile_key"
    ).rename(columns={"Seniority": "seniority", "YOE": "years_of_experience"})

    fact = transformed.reset_index(drop=True).copy()
    fact.insert(0, "application_key", range(1, len(fact) + 1))
    fact = fact.merge(dim_date[["date_key", "full_date"]], left_on="Application Date", right_on="full_date", how="left", validate="many_to_one")
    fact = fact.merge(dim_country, left_on="Country", right_on="country", how="left", validate="many_to_one")
    fact = fact.merge(dim_technology, left_on="Technology", right_on="technology", how="left", validate="many_to_one")
    fact = fact.merge(
        dim_candidate_profile,
        left_on=["Seniority", "YOE", "experience_band"],
        right_on=["seniority", "years_of_experience", "experience_band"],
        how="left", validate="many_to_one",
    )
    key_columns = ["date_key", "country_key", "technology_key", "candidate_profile_key"]
    if fact[key_columns].isna().any().any():
        raise ValueError("A fact row could not be mapped to a dimension surrogate key.")
    fact_applications = fact[[
        "application_key", *key_columns, "Code Challenge Score", "Technical Interview Score", "hired_flag"
    ]].rename(columns={
        "Code Challenge Score": "code_challenge_score",
        "Technical Interview Score": "technical_interview_score",
    })
    fact_applications["application_count"] = 1
    return {
        "dim_date": dim_date,
        "dim_country": dim_country,
        "dim_technology": dim_technology,
        "dim_candidate_profile": dim_candidate_profile,
        "fact_applications": fact_applications,
    }
