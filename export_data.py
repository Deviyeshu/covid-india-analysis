import pandas as pd
import sqlite3

db_path = r"C:\Users\yesas\Desktop\covid-india-analysis\data\covid.db"
conn = sqlite3.connect(db_path)
SAVE = r"C:\Users\yesas\Desktop\covid-india-analysis\data"

# Top 10 countries
pd.read_sql_query("""
SELECT country_region, MAX(confirmed) as total_confirmed,
MAX(deaths) as total_deaths,
ROUND(MAX(deaths)*100.0/MAX(confirmed),2) as death_rate_pct,
ROUND(MAX(recovered)*100.0/MAX(confirmed),2) as recovery_rate_pct
FROM covid_complete GROUP BY country_region
ORDER BY total_confirmed DESC LIMIT 10
""", conn).to_csv(f"{SAVE}\\top_countries.csv", index=False)

# India daily data
pd.read_sql_query("""
SELECT date, confirmed, deaths, recovered, active
FROM covid_complete WHERE country_region = 'India'
AND confirmed > 0 ORDER BY date
""", conn).to_csv(f"{SAVE}\\india_daily.csv", index=False)

# WHO region data
pd.read_sql_query("""
SELECT who_region, MAX(confirmed) as total_confirmed,
MAX(deaths) as total_deaths,
ROUND(MAX(deaths)*100.0/MAX(confirmed),2) as death_rate_pct
FROM full_grouped WHERE who_region != ''
GROUP BY who_region ORDER BY total_confirmed DESC
""", conn).to_csv(f"{SAVE}\\who_regions.csv", index=False)

# India monthly
pd.read_sql_query("""
SELECT strftime('%Y-%m', date) as year_month,
MAX(confirmed) as total_confirmed,
MAX(deaths) as total_deaths,
MAX(recovered) as total_recovered
FROM covid_complete WHERE country_region = 'India'
GROUP BY year_month ORDER BY year_month
""", conn).to_csv(f"{SAVE}\\india_monthly.csv", index=False)

conn.close()
print("✓ All CSV files exported for Power BI!")
print("Files saved:")
print("  - top_countries.csv")
print("  - india_daily.csv")
print("  - who_regions.csv")
print("  - india_monthly.csv")