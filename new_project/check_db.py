# list_dates.py
import sqlite3

conn = sqlite3.connect("algo.db")
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT datetime FROM data ORDER BY datetime")
rows = cursor.fetchall()

print("📅 Available Dates in 'data' table:")
for row in rows:
    print(row[0])

conn.close()