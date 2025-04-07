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

from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # this loads your HTML page

@app.route('/get_data', methods=['GET'])
def get_data():
    date = request.args.get('date')
    code = request.args.get('code', 'NIFTY')  # default is NIFTY if none provided

    conn = sqlite3.connect('algo.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM data WHERE datetime = ? AND code = ?", (date, code))
    ohlc_data = cursor.fetchall()

    cursor.execute("SELECT * FROM indicators WHERE datetime = ? AND code = ?", (date, code))
    indicators_data = cursor.fetchall()

    conn.close()

    return jsonify({
        "ohlc": ohlc_data,
        "indicators": indicators_data
    })

if __name__ == '__main__':
    app.run(debug=True)