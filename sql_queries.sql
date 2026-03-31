-- Project 5: Provincial Mental Health Outcomes
-- sql_queries.sql  —  SQL Programmer Hat
-- Load cchs_data.csv as table: cchs

-- ── 1. National mental health snapshot ───────────────────────────────────────
SELECT
    ROUND(AVG(good_mh) * 100, 1)          AS pct_good_excellent,
    ROUND(AVG(poor_mh) * 100, 1)          AS pct_fair_poor,
    ROUND(AVG(unmet_need) * 100, 1)       AS pct_unmet_need,
    ROUND(AVG(has_any_condition) * 100, 1) AS pct_with_condition,
    COUNT(*)                               AS respondents
FROM cchs;

-- ── 2. Province ranking ───────────────────────────────────────────────────────
SELECT
    province,
    COUNT(*)                                      AS n,
    ROUND(AVG(good_mh) * 100, 1)                 AS pct_good_mh,
    ROUND(AVG(poor_mh) * 100, 1)                 AS pct_poor_mh,
    ROUND(AVG(unmet_need) * 100, 1)              AS pct_unmet_need,
    ROUND(AVG(saw_mh_provider) * 100, 1)         AS pct_saw_provider
FROM cchs
GROUP BY province
ORDER BY pct_good_mh ASC;  -- worst first

-- ── 3. Age group breakdown ────────────────────────────────────────────────────
SELECT
    age_group,
    ROUND(AVG(good_mh) * 100, 1)                 AS pct_good_mh,
    ROUND(AVG(poor_mh) * 100, 1)                 AS pct_poor_mh,
    ROUND(AVG(unmet_need) * 100, 1)              AS pct_unmet_need,
    COUNT(*)                                      AS n
FROM cchs
GROUP BY age_group
ORDER BY pct_good_mh;

-- ── 4. Income group breakdown ─────────────────────────────────────────────────
SELECT
    income_group,
    ROUND(AVG(good_mh) * 100, 1)                 AS pct_good_mh,
    ROUND(AVG(poor_mh) * 100, 1)                 AS pct_poor_mh,
    ROUND(AVG(unmet_need) * 100, 1)              AS pct_unmet_need,
    COUNT(*)                                      AS n
FROM cchs
GROUP BY income_group
ORDER BY pct_good_mh;

-- ── 5. Indigenous vs. non-Indigenous gap ─────────────────────────────────────
SELECT
    indigenous,
    ROUND(AVG(good_mh) * 100, 1)                 AS pct_good_mh,
    ROUND(AVG(poor_mh) * 100, 1)                 AS pct_poor_mh,
    ROUND(AVG(unmet_need) * 100, 1)              AS pct_unmet_need,
    ROUND(AVG(saw_mh_provider) * 100, 1)         AS pct_saw_provider,
    COUNT(*)                                      AS n
FROM cchs
GROUP BY indigenous;

-- ── 6. Condition prevalence and unmet need ────────────────────────────────────
SELECT 'Depression'   AS condition,
    ROUND(AVG(Depression) * 100, 1)     AS prevalence_pct,
    ROUND(AVG(CASE WHEN Depression = 1 THEN unmet_need END) * 100, 1) AS pct_unmet
FROM cchs
UNION ALL
SELECT 'Anxiety',
    ROUND(AVG(Anxiety) * 100, 1),
    ROUND(AVG(CASE WHEN Anxiety = 1 THEN unmet_need END) * 100, 1)
FROM cchs
UNION ALL
SELECT 'PTSD',
    ROUND(AVG(PTSD) * 100, 1),
    ROUND(AVG(CASE WHEN PTSD = 1 THEN unmet_need END) * 100, 1)
FROM cchs
UNION ALL
SELECT 'Substance_Use',
    ROUND(AVG(Substance_Use) * 100, 1),
    ROUND(AVG(CASE WHEN Substance_Use = 1 THEN unmet_need END) * 100, 1)
FROM cchs
ORDER BY prevalence_pct DESC;

-- ── 7. High-risk group: low income + low education ───────────────────────────
SELECT
    income_group,
    education,
    ROUND(AVG(poor_mh) * 100, 1)     AS pct_poor_mh,
    ROUND(AVG(unmet_need) * 100, 1)  AS pct_unmet_need,
    COUNT(*)                          AS n
FROM cchs
WHERE income_group = '< $30K'
  AND education IN ('Less than HS', 'High School')
GROUP BY income_group, education;

-- ── 8. Province × income — equity gap ────────────────────────────────────────
SELECT
    province,
    income_group,
    ROUND(AVG(good_mh) * 100, 1)     AS pct_good_mh,
    COUNT(*)                          AS n
FROM cchs
GROUP BY province, income_group
ORDER BY province, pct_good_mh;
