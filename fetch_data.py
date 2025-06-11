import yfinance as yf
import pandas as pd
import sqlite3
import time

# Download 1 year of NIFTY data with retry logic
ticker = "^NSEI"
max_retries = 3
retry_delay = 30  # seconds

df = None
for attempt in range(max_retries):
    try:
        df = yf.download(ticker, period="1y", auto_adjust=False)
        if not df.empty:
            print("✅ Data download complete.")
            break
    except Exception as e:
        print(f"⚠️ Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
        time.sleep(retry_delay)

if df is None or df.empty:
    print("❌ Failed to download NIFTY data after several attempts.")
    exit()

df.reset_index(inplace=True)

# Handle possible MultiIndex columns
if isinstance(df.columns, pd.MultiIndex):
    df.columns = [col[0].lower() if col[0] != 'Date' else 'datetime' for col in df.columns]
else:
    df.rename(columns={
        "Date": "datetime",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close"
    }, inplace=True)

# Keep necessary columns
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

# Connect to SQLite
conn = sqlite3.connect("algo.db")
cursor = conn.cursor()

# Insert data into tables
for _, row in df.iterrows():
    # Extract values and convert safely
    datetime_str = str(row["datetime"])
    open_val = float(row["open"].item() if isinstance(row["open"], pd.Series) else row["open"])
    high_val = float(row["high"].item() if isinstance(row["high"], pd.Series) else row["high"])
    low_val = float(row["low"].item() if isinstance(row["low"], pd.Series) else row["low"])
    close_val = float(row["close"].item() if isinstance(row["close"], pd.Series) else row["close"])
    code = str(row["code"])
    sma_val = float(row["sma"])
    upper_val = float(row["upper"])
    lower_val = float(row["lower"])

    cursor.execute("INSERT OR REPLACE INTO data VALUES (?, ?, ?, ?, ?, ?)", (
        datetime_str, open_val, high_val, low_val, close_val, code
    ))

    cursor.execute("INSERT OR REPLACE INTO indicators VALUES (?, ?, ?, ?, ?)", (
        datetime_str, sma_val, upper_val, lower_val, code
    ))

conn.commit()
conn.close()

print("✅ Data inserted into database.")
