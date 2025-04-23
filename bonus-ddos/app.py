from flask import Flask, render_template, jsonify
import time
import random
from datetime import datetime

app = Flask(__name__)

# Simulate a simple in-memory store (vulnerable to memory exhaustion)
# Симулюємо просте сховище в пам'яті (вразливе до вичерпання пам'яті)
sessions = {}
products = [
    {"id": 1, "name": "Laptop", "price": 999.99, "stock": 10},
    {"id": 2, "name": "Smartphone", "price": 499.99, "stock": 15},
    {"id": 3, "name": "Headphones", "price": 99.99, "stock": 20},
]

def simulate_db_query():
    """Simulate slow database query / Симуляція повільного запиту до бази даних"""
    time.sleep(0.1)  # Simulate DB latency / Симуляція затримки БД

@app.route('/')
def index():
    """Main store page / Головна сторінка магазину"""
    # Create a new session for each visitor (memory leak)
    # Створюємо нову сесію для кожного відвідувача (витік пам'яті)
    session_id = random.randint(10000, 99999)
    sessions[session_id] = {
        'created_at': datetime.now(),
        'cart': [],
        'views': []
    }
    
    simulate_db_query()
    return render_template('store.html', products=products)

@app.route('/api/products')
def get_products():
    """Product API / API продуктів"""
    simulate_db_query()
    # Store page view in session (memory accumulation)
    # Зберігаємо перегляд сторінки в сесії (накопичення пам'яті)
    session_id = random.randint(10000, 99999)
    if session_id in sessions:
        sessions[session_id]['views'].append({
            'timestamp': datetime.now(),
            'page': 'products'
        })
    return jsonify(products)

@app.route('/api/stats')
def get_stats():
    """Server stats / Статистика сервера"""
    return jsonify({
        'active_sessions': len(sessions),
        'total_products': len(products),
        'server_time': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 