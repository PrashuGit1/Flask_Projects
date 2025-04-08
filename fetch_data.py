import yfinance as yf
import pandas as pd
import sqlite3

# Download 1 year of NIFTY data
df = yf.download("^NSEI", period="1y", auto_adjust=False)
df.reset_index(inplace=True)

# Check if the DataFrame has multi-level columns (caused by multiple tickers)
if isinstance(df.columns, pd.MultiIndex):
    # Flatten the columns
    df.columns = [col[0].lower() if col[0] != 'Date' else 'datetime' for col in df.columns]
else:
    df.rename(columns={
        "Date": "datetime",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close"
    }, inplace=True)

# Keep only necessary columns
df = df[["datetime", "open", "high", "low", "close"]]
df["code"] = "NIFTY"

# Calculate Bollinger Bands
df["sma"] = df["close"].rolling(window=20).mean()
df["std"] = df["close"].rolling(window=20).std()
df["upper"] = df["sma"] + 2 * df["std"]
df["lower"] = df["sma"] - 2 * df["std"]
df.dropna(inplace=True)

# Format datetime
df["datetime"] = df["datetime"].dt.strftime("%Y-%m-%d")

# Connect to DB
conn = sqlite3.connect("algo.db")
cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("INSERT OR REPLACE INTO data VALUES (?, ?, ?, ?, ?, ?)", (
        row["datetime"], float(row["open"]), float(row["high"]),
        float(row["low"]), float(row["close"]), row["code"]
    ))

    cursor.execute("INSERT OR REPLACE INTO indicators VALUES (?, ?, ?, ?, ?)", (
        row["datetime"], float(row["sma"]), float(row["upper"]),
        float(row["lower"]), row["code"]
    ))

conn.commit()
conn.close()

print("✅ Data inserted into database.")