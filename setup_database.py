import pandas as pd
import sqlite3

# ---- LOAD ALL CSV FILES ----
main = pd.read_csv(r"C:\Users\yesas\Desktop\covid-india-analysis\data\covid_19_clean_complete.csv")
day_wise = pd.read_csv(r"C:\Users\yesas\Desktop\covid-india-analysis\data\day_wise.csv")
full_grouped = pd.read_csv(r"C:\Users\yesas\Desktop\covid-india-analysis\data\full_grouped.csv")

print(f"Main file: {main.shape}")
print(f"Day wise: {day_wise.shape}")
print(f"Full grouped: {full_grouped.shape}")

# ---- CLEAN COLUMN NAMES ----
# Remove spaces and special characters from column names
main.columns = main.columns.str.replace('/', '_').str.replace(' ', '_').str.lower()
day_wise.columns = day_wise.columns.str.replace('/', '_').str.replace(' ', '_').str.lower()
full_grouped.columns = full_grouped.columns.str.replace('/', '_').str.replace(' ', '_').str.lower()

print(f"\nMain columns: {list(main.columns)}")
print(f"Day wise columns: {list(day_wise.columns)}")
print(f"Full grouped columns: {list(full_grouped.columns)}")

# ---- CREATE SQLITE DATABASE ----
db_path = r"C:\Users\yesas\Desktop\covid-india-analysis\data\covid.db"
conn = sqlite3.connect(db_path)

# Save all tables to database
main.to_sql('covid_complete', conn, if_exists='replace', index=False)
day_wise.to_sql('day_wise', conn, if_exists='replace', index=False)
full_grouped.to_sql('full_grouped', conn, if_exists='replace', index=False)

print(f"\n✓ Database created successfully!")
print(f"✓ Tables created: covid_complete, day_wise, full_grouped")

# ---- VERIFY TABLES ----
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"✓ Tables in database: {tables}")

# ---- CHECK ROW COUNTS ----
for table in ['covid_complete', 'day_wise', 'full_grouped']:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"  {table}: {count} rows")

conn.close()
print(f"\n✓ Database saved to: {db_path}")
print("→ Now open DB Browser for SQLite to write SQL queries!")