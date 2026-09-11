import argparse
from pathlib import Path

from src.dimensional_model import build_dimensional_model
from src.extract import extract_candidates
from src.transform import apply_business_rules, prepare_candidates


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the recruitment dimensional data warehouse.")
    parser.add_argument("--skip-load", action="store_true", help="Build and validate dimensional datasets without PostgreSQL.")
    args = parser.parse_args()
    raw = extract_candidates()
    prepared = prepare_candidates(raw)
    transformed = apply_business_rules(prepared)
    tables = build_dimensional_model(transformed)
    print(f"Prepared applications: {len(transformed):,}")
    print(f"Hired applications: {int(transformed['hired_flag'].sum()):,}")
    for name, table in tables.items():
        print(f"{name}: {len(table):,} rows")
    if not args.skip_load:
        from src.load import load_to_postgres
        load_to_postgres(tables)
        print("Loaded successfully into PostgreSQL.")


if __name__ == "__main__":
    main()
