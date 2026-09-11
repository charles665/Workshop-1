-- R1. Hiring trends by month
SELECT d.year, d.month_number, d.month_name,
       SUM(f.application_count) AS applications,
       SUM(f.hired_flag) AS hired_candidates,
       ROUND(100.0 * SUM(f.hired_flag) / NULLIF(SUM(f.application_count), 0), 2) AS hiring_rate_pct
FROM recruitment_dw.fact_applications f
JOIN recruitment_dw.dim_date d ON d.date_key = f.date_key
GROUP BY d.year, d.month_number, d.month_name
ORDER BY d.year, d.month_number;

-- R2. Technology analysis
SELECT t.technology,
       SUM(f.application_count) AS applications,
       SUM(f.hired_flag) AS hired_candidates,
       ROUND(100.0 * SUM(f.hired_flag) / NULLIF(SUM(f.application_count), 0), 2) AS hiring_rate_pct
FROM recruitment_dw.fact_applications f
JOIN recruitment_dw.dim_technology t ON t.technology_key = f.technology_key
GROUP BY t.technology
ORDER BY hired_candidates DESC, hiring_rate_pct DESC;

-- R3. Candidate profile analysis
SELECT p.seniority, p.experience_band,
       SUM(f.application_count) AS applications,
       SUM(f.hired_flag) AS hired_candidates,
       ROUND(100.0 * SUM(f.hired_flag) / NULLIF(SUM(f.application_count), 0), 2) AS hiring_rate_pct
FROM recruitment_dw.fact_applications f
JOIN recruitment_dw.dim_candidate_profile p ON p.candidate_profile_key = f.candidate_profile_key
GROUP BY p.seniority, p.experience_band
ORDER BY p.seniority, p.experience_band;

-- R4. Geographic recruitment activity and outcomes
SELECT c.country,
       SUM(f.application_count) AS applications,
       SUM(f.hired_flag) AS hired_candidates,
       ROUND(100.0 * SUM(f.hired_flag) / NULLIF(SUM(f.application_count), 0), 2) AS hiring_rate_pct
FROM recruitment_dw.fact_applications f
JOIN recruitment_dw.dim_country c ON c.country_key = f.country_key
GROUP BY c.country
HAVING SUM(f.application_count) >= 30
ORDER BY hired_candidates DESC, hiring_rate_pct DESC;

-- R5. Hiring outcome by assessment-score segment
SELECT
    CASE
        WHEN f.code_challenge_score >= 7 AND f.technical_interview_score >= 7 THEN 'Both scores >= 7'
        WHEN f.code_challenge_score >= 7 AND f.technical_interview_score < 7 THEN 'Code >= 7; interview < 7'
        WHEN f.code_challenge_score < 7 AND f.technical_interview_score >= 7 THEN 'Code < 7; interview >= 7'
        ELSE 'Both scores < 7'
    END AS assessment_segment,
    SUM(f.application_count) AS applications,
    SUM(f.hired_flag) AS hired_candidates,
    ROUND(100.0 * SUM(f.hired_flag) / NULLIF(SUM(f.application_count), 0), 2) AS hiring_rate_pct
FROM recruitment_dw.fact_applications f
GROUP BY assessment_segment
ORDER BY applications DESC;
