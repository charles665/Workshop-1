import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "sql" / "create_tables.sql"


def _connection_string() -> str:
    load_dotenv(PROJECT_ROOT / ".env")
    values = {key: os.getenv(key) for key in ["POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD"]}
    if not all(values.values()):
        raise RuntimeError("Create .env from .env.example and set all PostgreSQL values before loading.")
    return "host={POSTGRES_HOST} port={POSTGRES_PORT} dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD}".format(**values)


def load_to_postgres(tables: dict[str, pd.DataFrame]) -> None:
    """Recreate the workshop schema and load dimensions before the fact table."""
    with psycopg.connect(_connection_string()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(SCHEMA_PATH.read_text(encoding="utf-8"))
            for table_name in ["dim_date", "dim_country", "dim_technology", "dim_candidate_profile", "fact_applications"]:
                frame = tables[table_name].copy()
                for column in frame.select_dtypes(include=["datetime64[ns]"]).columns:
                    frame[column] = frame[column].dt.date
                columns = list(frame.columns)
                placeholders = ", ".join(["%s"] * len(columns))
                statement = f"INSERT INTO recruitment_dw.{table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                cursor.executemany(statement, list(frame.itertuples(index=False, name=None)))
        connection.commit()
