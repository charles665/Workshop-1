# Instructions to present the diagrams

The Mermaid sources in `diagrams/` are the authoritative diagrams. GitHub renders them automatically; for a slide or report, open the Markdown preview and export or screenshot it.

## Program flow

Draw, in this order: **oval: Start** → **parallelogram: Read `data/raw/candidates.csv`** → **rectangle: Create raw DataFrame** → **rectangle: Prepare dates, types and categories** → **diamond: Are required fields valid?**. The No branch goes to **parallelogram: Report data-quality error** and then **oval: End**. The Yes branch goes to **rectangle: Apply HIRED rule and experience band** → **rectangle: Create dimensions and surrogate keys** → **rectangle: Map keys and create Fact_Applications** → **diamond: Was `--skip-load` used?**. Yes goes to **parallelogram: Print ETL summary** → End. No goes to **rectangle: Create PostgreSQL schema** → **rectangle: Load dimensions** → **rectangle: Load fact table** → **parallelogram: Run validation SQL/KPIs** → End.

## Architecture

Draw seven boxes left to right: `Source CSV` → `Python/Pandas Extract` → `Preparation` → `Business transformation (HIRED)` → `Dimensional transformation (SKs + fact)` → `PostgreSQL recruitment_dw` → `SQL/KPIs and Power BI` → `Recruitment decisions`. Add a second arrow from PostgreSQL directly to Power BI.

## Star schema

Place `Fact_Applications` in the centre. Put `Dim_Date` above-left, `Dim_Country` below-left, `Dim_Technology` above-right and `Dim_Candidate_Profile` below-right. Connect every dimension PK to its matching fact FK with a one-to-many line. Copy field names only from `sql/create_tables.sql`; this makes the drawing equal to the implemented SQL and ETL.
