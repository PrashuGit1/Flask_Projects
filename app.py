from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def get_data_for_date(date):
    conn = sqlite3.connect('algo.db')
    cursor = conn.cursor()

    # Fetch OHLC data
    cursor.execute("SELECT open, high, low, close FROM data WHERE datetime = ?", (date,))
    ohlc = cursor.fetchone()

    # Fetch indicators
    cursor.execute("SELECT sma, upper, lower FROM indicators WHERE datetime = ?", (date,))
    indicators = cursor.fetchone()

    conn.close()

    return {
        "data": {
            "open": ohlc[0] if ohlc else None,
            "high": ohlc[1] if ohlc else None,
            "low": ohlc[2] if ohlc else None,
            "close": ohlc[3] if ohlc else None
        },
        "indicators": {
            "sma": indicators[0] if indicators else None,
            "upper": indicators[1] if indicators else None,
            "lower": indicators[2] if indicators else None
        }
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def data():
    date = request.args.get('date')
    if not date:
        return jsonify({"error": "Missing date"}), 400
    result = get_data_for_date(date)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)