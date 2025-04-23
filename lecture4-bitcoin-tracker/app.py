from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import os

app = Flask(__name__)

# Coinbase API endpoint / Кінцева точка API Coinbase
COINBASE_API_URL = "https://api.coinbase.com/v2/prices/BTC-USD/spot"

def get_bitcoin_price():
    """
    Get current Bitcoin price from Coinbase
    Отримати поточну ціну Bitcoin з Coinbase
    """
    try:
        response = requests.get(COINBASE_API_URL)
        data = response.json()
        return float(data["data"]["amount"])
    except Exception as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None

@app.route('/')
def index():
    """
    Main dashboard page
    Головна сторінка панелі
    """
    current_price = get_bitcoin_price()
    return render_template('dashboard.html', 
                         price=current_price,
                         last_updated=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/api/price')
def get_price():
    """
    API endpoint for current price
    Кінцева точка API для поточної ціни
    """
    price = get_bitcoin_price()
    if price is None:
        return jsonify({"error": "Failed to fetch price"}), 500
    return jsonify({
        "price": price,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 