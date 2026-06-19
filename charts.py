import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings("ignore")

# ---- CONNECT TO DATABASE ----
db_path = r"C:\Users\yesas\Desktop\covid-india-analysis\data\covid.db"
conn = sqlite3.connect(db_path)

# ---- STYLE ----
plt.rcParams.update({
    "figure.facecolor": "#FAFAFA",
    "axes.facecolor": "#FAFAFA",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.titlepad": 12,
    "font.family": "DejaVu Sans",
})
COLORS = ["#1D9E75", "#534AB7", "#D85A30", "#BA7517", "#185FA5",
          "#A32D2D", "#3B6D11", "#D4537E"]
SAVE = r"C:\Users\yesas\Desktop\covid-india-analysis\visuals"

# ============================================================
# CHART 1: Top 10 Most Affected Countries
# ============================================================
query1 = """
SELECT country_region, MAX(confirmed) as total_confirmed
FROM covid_complete
GROUP BY country_region
ORDER BY total_confirmed DESC
LIMIT 10
"""
df1 = pd.read_sql_query(query1, conn)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(df1['country_region'][::-1], df1['total_confirmed'][::-1],
               color=COLORS[0], edgecolor="none")
for bar, val in zip(bars, df1['total_confirmed'][::-1]):
    ax.text(bar.get_width() + 10000, bar.get_y() + bar.get_height()/2,
            f'{val:,.0f}', va='center', fontsize=9)
ax.set_title("Top 10 Most Affected Countries (Total Confirmed Cases)")
ax.set_xlabel("Total Confirmed Cases")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
plt.tight_layout()
plt.savefig(f"{SAVE}\\chart1_top_countries.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 1 saved: top countries")

# ============================================================
# CHART 2: India Daily Growth (Confirmed Cases Over Time)
# ============================================================
query2 = """
SELECT date, confirmed, deaths, recovered, active
FROM covid_complete
WHERE country_region = 'India'
AND confirmed > 0
ORDER BY date
"""
df2 = pd.read_sql_query(query2, conn)
df2['date'] = pd.to_datetime(df2['date'])

fig, ax = plt.subplots(figsize=(12, 6))
ax.fill_between(df2['date'], df2['confirmed'], alpha=0.3, color=COLORS[2], label='Confirmed')
ax.fill_between(df2['date'], df2['recovered'], alpha=0.5, color=COLORS[0], label='Recovered')
ax.fill_between(df2['date'], df2['deaths'], alpha=0.7, color=COLORS[7], label='Deaths')
ax.plot(df2['date'], df2['confirmed'], color=COLORS[2], linewidth=1.5)
ax.set_title("India COVID-19 Cases Growth (Jan - Jul 2020)")
ax.set_xlabel("Date")
ax.set_ylabel("Number of Cases")
ax.legend(fontsize=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M' if x >= 1e6 else f'{x/1e3:.0f}K'))
plt.tight_layout()
plt.savefig(f"{SAVE}\\chart2_india_growth.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 2 saved: India growth")

# ============================================================
# CHART 3: India vs World Death Rate Comparison
# ============================================================
countries = ['India', 'US', 'Brazil', 'Russia', 'United Kingdom']
query3 = f"""
SELECT country_region,
    MAX(confirmed) as total_confirmed,
    MAX(deaths) as total_deaths,
    ROUND(MAX(deaths) * 100.0 / MAX(confirmed), 2) as death_rate_pct
FROM covid_complete
WHERE country_region IN ('India', 'US', 'Brazil', 'Russia', 'United Kingdom')
GROUP BY country_region
ORDER BY death_rate_pct DESC
"""
df3 = pd.read_sql_query(query3, conn)

fig, ax = plt.subplots(figsize=(9, 6))
colors = [COLORS[2] if r > 3 else COLORS[0] for r in df3['death_rate_pct']]
bars = ax.bar(df3['country_region'], df3['death_rate_pct'],
              color=colors, edgecolor="none", width=0.5)
for bar, val in zip(bars, df3['death_rate_pct']):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.1,
            f'{val}%', ha='center', fontsize=11, fontweight='bold')
ax.axhline(y=3.97, color='gray', linestyle='--', linewidth=1.5,
           label='World Average (3.97%)')
ax.set_title("Death Rate Comparison — India vs Major Countries")
ax.set_ylabel("Death Rate (%)")
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(f"{SAVE}\\chart3_death_rate_comparison.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 3 saved: death rate comparison")

# ============================================================
# CHART 4: WHO Region Analysis
# ============================================================
query4 = """
SELECT who_region,
    MAX(confirmed) as total_confirmed,
    MAX(deaths) as total_deaths,
    ROUND(MAX(deaths) * 100.0 / MAX(confirmed), 2) as death_rate_pct
FROM full_grouped
WHERE who_region != ''
GROUP BY who_region
ORDER BY total_confirmed DESC
"""
df4 = pd.read_sql_query(query4, conn)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(df4['who_region'][::-1], df4['total_confirmed'][::-1],
               color=COLORS[:len(df4)], edgecolor="none")
for bar, val in zip(bars, df4['total_confirmed'][::-1]):
    ax.text(bar.get_width() + 10000, bar.get_y() + bar.get_height()/2,
            f'{val:,.0f}', va='center', fontsize=9)
ax.set_title("COVID-19 Cases by WHO Region")
ax.set_xlabel("Total Confirmed Cases")
plt.tight_layout()
plt.savefig(f"{SAVE}\\chart4_who_region.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 4 saved: WHO region")

# ============================================================
# CHART 5: India Monthly Progress
# ============================================================
query5 = """
SELECT strftime('%Y-%m', date) as year_month,
    MAX(confirmed) as total_confirmed,
    MAX(deaths) as total_deaths,
    MAX(recovered) as total_recovered
FROM covid_complete
WHERE country_region = 'India'
GROUP BY year_month
ORDER BY year_month
"""
df5 = pd.read_sql_query(query5, conn)

fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(df5))
ax.bar(x, df5['total_confirmed'], color=COLORS[2], alpha=0.7,
       label='Confirmed', width=0.6)
ax.bar(x, df5['total_recovered'], color=COLORS[0], alpha=0.9,
       label='Recovered', width=0.6)
ax.bar(x, df5['total_deaths'], color=COLORS[7], alpha=0.9,
       label='Deaths', width=0.6)
ax.set_xticks(list(x))
ax.set_xticklabels(df5['year_month'], rotation=45, ha='right')
ax.set_title("India COVID-19 Monthly Progress")
ax.set_ylabel("Total Cases")
ax.legend(fontsize=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M' if x >= 1e6 else f'{x/1e3:.0f}K'))
plt.tight_layout()
plt.savefig(f"{SAVE}\\chart5_india_monthly.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 5 saved: India monthly progress")

# ============================================================
# CHART 6: Top Countries by Recovery Rate
# ============================================================
query6 = """
SELECT country_region,
    ROUND(MAX(recovered) * 100.0 / MAX(confirmed), 2) as recovery_rate_pct
FROM covid_complete
GROUP BY country_region
HAVING MAX(confirmed) > 10000
ORDER BY recovery_rate_pct DESC
LIMIT 10
"""
df6 = pd.read_sql_query(query6, conn)

fig, ax = plt.subplots(figsize=(10, 6))
colors = [COLORS[0] if c == 'India' else COLORS[1] for c in df6['country_region']]
bars = ax.barh(df6['country_region'][::-1], df6['recovery_rate_pct'][::-1],
               color=colors[::-1], edgecolor="none")
for bar, val in zip(bars, df6['recovery_rate_pct'][::-1]):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f'{val}%', va='center', fontsize=10, fontweight='bold')
ax.set_title("Top 10 Countries by Recovery Rate\n(Min 10,000 Confirmed Cases)")
ax.set_xlabel("Recovery Rate (%)")
plt.tight_layout()
plt.savefig(f"{SAVE}\\chart6_recovery_rate.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 6 saved: recovery rate")

conn.close()
print("\n✓ All 6 charts saved to visuals folder!")
print("→ Now build Power BI dashboard!")