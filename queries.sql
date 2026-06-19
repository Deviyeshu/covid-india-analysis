-- ============================================================
-- COVID-19 INDIA ANALYSIS — SQL QUERIES
-- Run these in DB Browser for SQLite
-- ============================================================

-- ============================================================
-- QUERY 1: India's Overall COVID Summary
-- ============================================================
SELECT 
    country_region,
    MAX(confirmed) as total_confirmed,
    MAX(deaths) as total_deaths,
    MAX(recovered) as total_recovered,
    MAX(active) as total_active,
    ROUND(MAX(deaths) * 100.0 / MAX(confirmed), 2) as death_rate_pct,
    ROUND(MAX(recovered) * 100.0 / MAX(confirmed), 2) as recovery_rate_pct
FROM covid_complete
WHERE country_region = 'India'
GROUP BY country_region;

-- ============================================================
-- QUERY 2: Top 10 Most Affected Countries
-- ============================================================
SELECT 
    country_region,
    MAX(confirmed) as total_confirmed,
    MAX(deaths) as total_deaths,
    MAX(recovered) as total_recovered,
    ROUND(MAX(deaths) * 100.0 / MAX(confirmed), 2) as death_rate_pct
FROM covid_complete
GROUP BY country_region
ORDER BY total_confirmed DESC
LIMIT 10;

-- ============================================================
-- QUERY 3: India vs Top 5 Countries Comparison
-- ============================================================
SELECT 
    country_region,
    MAX(confirmed) as total_confirmed,
    MAX(deaths) as total_deaths,
    ROUND(MAX(deaths) * 100.0 / MAX(confirmed), 2) as death_rate_pct,
    ROUND(MAX(recovered) * 100.0 / MAX(confirmed), 2) as recovery_rate_pct
FROM covid_complete
WHERE country_region IN ('India', 'US', 'Brazil', 'Russia', 'UK')
GROUP BY country_region
ORDER BY total_confirmed DESC;

-- ============================================================
-- QUERY 4: WHO Region wise Analysis
-- ============================================================
SELECT 
    who_region,
    COUNT(DISTINCT country_region) as total_countries,
    MAX(confirmed) as total_confirmed,
    MAX(deaths) as total_deaths,
    ROUND(MAX(deaths) * 100.0 / MAX(confirmed), 2) as death_rate_pct
FROM full_grouped
WHERE who_region != ''
GROUP BY who_region
ORDER BY total_confirmed DESC;

-- ============================================================
-- QUERY 5: India Monthly Growth Rate
-- ============================================================
SELECT 
    strftime('%Y-%m', date) as year_month,
    MAX(confirmed) as total_confirmed,
    MAX(deaths) as total_deaths,
    MAX(recovered) as total_recovered,
    MAX(active) as active_cases
FROM covid_complete
WHERE country_region = 'India'
GROUP BY year_month
ORDER BY year_month;

-- ============================================================
-- QUERY 6: Daily New Cases Worldwide (Peak Days)
-- ============================================================
SELECT 
    date,
    new_cases,
    new_deaths,
    new_recovered,
    confirmed
FROM day_wise
ORDER BY new_cases DESC
LIMIT 10;

-- ============================================================
-- QUERY 7: Countries with Best Recovery Rate
-- (minimum 10000 confirmed cases)
-- ============================================================
SELECT 
    country_region,
    MAX(confirmed) as total_confirmed,
    MAX(recovered) as total_recovered,
    ROUND(MAX(recovered) * 100.0 / MAX(confirmed), 2) as recovery_rate_pct
FROM covid_complete
GROUP BY country_region
HAVING total_confirmed > 10000
ORDER BY recovery_rate_pct DESC
LIMIT 10;

-- ============================================================
-- QUERY 8: India vs World Death Rate Comparison
-- ============================================================
SELECT
    'India' as region,
    ROUND(MAX(deaths) * 100.0 / MAX(confirmed), 2) as death_rate_pct
FROM covid_complete
WHERE country_region = 'India'

UNION ALL

SELECT
    'World' as region,
    ROUND(SUM(deaths) * 100.0 / SUM(confirmed), 2) as death_rate_pct
FROM day_wise
WHERE date = (SELECT MAX(date) FROM day_wise);

-- ============================================================
-- QUERY 9: Fastest Growing Countries (New Cases)
-- ============================================================
SELECT 
    country_region,
    MAX(new_cases) as peak_daily_cases,
    MAX(confirmed) as total_confirmed
FROM full_grouped
GROUP BY country_region
ORDER BY peak_daily_cases DESC
LIMIT 10;

-- ============================================================
-- QUERY 10: India Recovery Progress Over Time
-- ============================================================
SELECT 
    date,
    confirmed,
    deaths,
    recovered,
    active,
    ROUND(recovered * 100.0 / confirmed, 2) as recovery_rate_pct
FROM covid_complete
WHERE country_region = 'India'
AND confirmed > 0
ORDER BY date;