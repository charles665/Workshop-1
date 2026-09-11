-- Expected row counts after a successful load.
SELECT 'dim_date' AS table_name, COUNT(*) AS row_count FROM recruitment_dw.dim_date
UNION ALL SELECT 'dim_country', COUNT(*) FROM recruitment_dw.dim_country
UNION ALL SELECT 'dim_technology', COUNT(*) FROM recruitment_dw.dim_technology
UNION ALL SELECT 'dim_candidate_profile', COUNT(*) FROM recruitment_dw.dim_candidate_profile
UNION ALL SELECT 'fact_applications', COUNT(*) FROM recruitment_dw.fact_applications;

-- Must return zero rows: all fact foreign keys must resolve to dimensions.
SELECT f.application_key
FROM recruitment_dw.fact_applications f
LEFT JOIN recruitment_dw.dim_date d ON d.date_key = f.date_key
LEFT JOIN recruitment_dw.dim_country c ON c.country_key = f.country_key
LEFT JOIN recruitment_dw.dim_technology t ON t.technology_key = f.technology_key
LEFT JOIN recruitment_dw.dim_candidate_profile p ON p.candidate_profile_key = f.candidate_profile_key
WHERE d.date_key IS NULL OR c.country_key IS NULL OR t.technology_key IS NULL OR p.candidate_profile_key IS NULL;

-- The HIRED flag must exactly match the business rule; expected mismatches: zero.
SELECT COUNT(*) AS hired_rule_mismatches
FROM recruitment_dw.fact_applications
WHERE hired_flag <> CASE
    WHEN code_challenge_score >= 7 AND technical_interview_score >= 7 THEN 1 ELSE 0 END;
