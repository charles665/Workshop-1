# Star schema

```mermaid
erDiagram
    DIM_DATE ||--o{ FACT_APPLICATIONS : date_key
    DIM_COUNTRY ||--o{ FACT_APPLICATIONS : country_key
    DIM_TECHNOLOGY ||--o{ FACT_APPLICATIONS : technology_key
    DIM_CANDIDATE_PROFILE ||--o{ FACT_APPLICATIONS : candidate_profile_key
    DIM_DATE { int date_key PK\n date full_date\n int year\n int quarter\n int month_number\n string month_name }
    DIM_COUNTRY { int country_key PK\n string country }
    DIM_TECHNOLOGY { int technology_key PK\n string technology }
    DIM_CANDIDATE_PROFILE { int candidate_profile_key PK\n string seniority\n int years_of_experience\n string experience_band }
    FACT_APPLICATIONS { bigint application_key PK\n int date_key FK\n int country_key FK\n int technology_key FK\n int candidate_profile_key FK\n int code_challenge_score\n int technical_interview_score\n int hired_flag\n int application_count }
```
