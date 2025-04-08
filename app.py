from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def query_data(date):
    conn = sqlite3.connect("algo.db")
    cursor = conn.cursor()

    # Fetch OHLC data for the date
    cursor.execute("SELECT datetime, open, high, low, close FROM data WHERE datetime = ?", (date,))
    ohlc = cursor.fetchone()

    # Fetch Bollinger Band indicators for the date
    cursor.execute("SELECT datetime, sma, upper, lower FROM indicators WHERE datetime = ?", (date,))
    indicators = cursor.fetchone()

    conn.close()
    return ohlc, indicators

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-data', methods=['GET'])  # <- Changed from POST to GET
def get_data():
    date = request.args.get('date')       # <- Changed from form to args
    print(f"📅 Received request for date: {date}")

    ohlc, indicators = query_data(date)
    print(f"📊 OHLC: {ohlc}")
    print(f"📈 Indicators: {indicators}")

    if not ohlc or not indicators:
        return jsonify({'error': 'No data found for the given date'})

    return jsonify({
        'ohlc': {
            'datetime': ohlc[0],
            'open': ohlc[1],
            'high': ohlc[2],
            'low': ohlc[3],
            'close': ohlc[4]
        },
        'indicators': {
            'sma': indicators[1],
            'upper': indicators[2],
            'lower': indicators[3]
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
