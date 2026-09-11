CREATE SCHEMA IF NOT EXISTS recruitment_dw;

DROP TABLE IF EXISTS recruitment_dw.fact_applications;
DROP TABLE IF EXISTS recruitment_dw.dim_candidate_profile;
DROP TABLE IF EXISTS recruitment_dw.dim_technology;
DROP TABLE IF EXISTS recruitment_dw.dim_country;
DROP TABLE IF EXISTS recruitment_dw.dim_date;

CREATE TABLE recruitment_dw.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    year SMALLINT NOT NULL,
    quarter SMALLINT NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    month_number SMALLINT NOT NULL CHECK (month_number BETWEEN 1 AND 12),
    month_name VARCHAR(20) NOT NULL
);

CREATE TABLE recruitment_dw.dim_country (
    country_key INTEGER PRIMARY KEY,
    country VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE recruitment_dw.dim_technology (
    technology_key INTEGER PRIMARY KEY,
    technology VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE recruitment_dw.dim_candidate_profile (
    candidate_profile_key INTEGER PRIMARY KEY,
    seniority VARCHAR(30) NOT NULL,
    years_of_experience SMALLINT NOT NULL CHECK (years_of_experience >= 0),
    experience_band VARCHAR(20) NOT NULL,
    UNIQUE (seniority, years_of_experience, experience_band)
);

CREATE TABLE recruitment_dw.fact_applications (
    application_key BIGINT PRIMARY KEY,
    date_key INTEGER NOT NULL REFERENCES recruitment_dw.dim_date(date_key),
    country_key INTEGER NOT NULL REFERENCES recruitment_dw.dim_country(country_key),
    technology_key INTEGER NOT NULL REFERENCES recruitment_dw.dim_technology(technology_key),
    candidate_profile_key INTEGER NOT NULL REFERENCES recruitment_dw.dim_candidate_profile(candidate_profile_key),
    code_challenge_score SMALLINT NOT NULL CHECK (code_challenge_score BETWEEN 0 AND 10),
    technical_interview_score SMALLINT NOT NULL CHECK (technical_interview_score BETWEEN 0 AND 10),
    hired_flag SMALLINT NOT NULL CHECK (hired_flag IN (0, 1)),
    application_count SMALLINT NOT NULL DEFAULT 1 CHECK (application_count = 1)
);

CREATE INDEX idx_fact_date ON recruitment_dw.fact_applications(date_key);
CREATE INDEX idx_fact_country ON recruitment_dw.fact_applications(country_key);
CREATE INDEX idx_fact_technology ON recruitment_dw.fact_applications(technology_key);
CREATE INDEX idx_fact_profile ON recruitment_dw.fact_applications(candidate_profile_key);
