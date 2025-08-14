import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("algo.db")
cursor = conn.cursor()

# Create 'data' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        datetime TEXT PRIMARY KEY,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        code TEXT
    )
''')

# Create 'indicators' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS indicators (
        datetime TEXT PRIMARY KEY,
        sma REAL,
        upper REAL,
        lower REAL,
        code TEXT
    )
''')

conn.commit()
conn.close()

print("✅ Database and tables created successfully with 'code' column.")