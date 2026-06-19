# 🦠 COVID-19 India & Global Analysis

> SQL-driven analysis of global COVID-19 data (Jan-Jul 2020) with focus 
> on India's pandemic trajectory compared to other major countries.

---

## 🎯 Project Objective
- How did India's COVID-19 outcomes compare to other major countries?
- Which WHO regions were most affected?
- What was India's death rate vs recovery rate vs world average?
- How did cases grow month over month in India?

---

## 📈 Key Findings
- **India's death rate (2.26%) was LOWER than the world average (3.97%)**
- India ranked **#3 globally** in total confirmed cases (1.48M) by July 2020
- **Americas region** accounted for 57.82% of all global cases
- India's **recovery rate reached 64.26%** by end of July 2020
- **Qatar had the highest recovery rate (97.02%)** among countries with 10,000+ cases
- **UK had the highest death rate (15.25%)** among major countries

---

## 🔧 Tools Used
- **SQL** (SQLite) — 10 analytical queries for data extraction
- Python, Pandas, Matplotlib — data processing and visualization
- Power BI — interactive dashboard
- Dataset: COVID-19 Global Dataset from Kaggle

---

## 💾 SQL Queries
All analysis was performed using SQL queries on a SQLite database 
built from 3 source tables (49,068+ records). See [queries.sql](sql/queries.sql) 
for all 10 queries including:
- Country-wise aggregation with death/recovery rate calculations
- WHO region grouping and comparison
- Time-series monthly aggregation using `strftime()`
- Multi-table UNION query for India vs World comparison

---

## 📊 Power BI Dashboard
![Dashboard](visuals/dashboard_final.png)

---

## 📉 Charts
![Top Countries](visuals/chart1_top_countries.png)
![India Growth](visuals/chart2_india_growth.png)
![Death Rate Comparison](visuals/chart3_death_rate_comparison.png)
![WHO Region](visuals/chart4_who_region.png)
![India Monthly](visuals/chart5_india_monthly.png)
![Recovery Rate](visuals/chart6_recovery_rate.png)

---

## 💡 Key Insights
1. **India managed the pandemic relatively well** in terms of death 
   rate — significantly below global average despite having the 
   3rd highest case count
2. **Healthcare capacity matters more than case count** — Qatar and 
   smaller nations achieved much higher recovery rates than larger countries
3. **Regional disparity is significant** — Americas alone accounted 
   for more than half of global cases

---

## 👩‍💻 About
Built by **Parnam Yesaswini Devi** — MSc Statistics,
Sri Venkateswara University
Actively seeking Data Analyst roles in South India and remote.

📧 [parnamyesaswinidevi@gmail.com] | 🔗 [linkedin.com/in/yesaswini-devi-parnam]

---

*Note: This analysis covers data through July 2020 as per the source 
dataset and is intended as a demonstration of SQL, Python, and data 
visualization skills.*
