from flask import Flask, render_template, jsonify
import time

app = Flask(__name__)

@app.route('/')
def index():
    """
    Main page with interactive browser demo
    Головна сторінка з інтерактивною демонстрацією браузера
    """
    return render_template('index.html')

@app.route('/api/example', methods=['GET', 'POST'])
def example_api():
    """
    Example API endpoint for demonstration
    Приклад API endpoint для демонстрації
    """
    # Simulate processing delay / Симуляція затримки обробки
    time.sleep(1)
    
    return jsonify({
        'message': 'Success',
        'timestamp': time.time()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000) 