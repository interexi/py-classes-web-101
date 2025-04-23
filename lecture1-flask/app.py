from flask import Flask, render_template
import os

# Initialize Flask application / Ініціалізація Flask додатку
app = Flask(__name__)

# Route for the main page / Маршрут для головної сторінки
@app.route('/')
def index():
    """
    Main page route
    Маршрут головної сторінки
    """
    return render_template('index.html', title='Flask Demo')

# Route with parameter / Маршрут з параметром
@app.route('/hello/<name>')
def hello(name):
    """
    Personalized greeting route
    Маршрут для персоналізованого привітання
    """
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    # Run the application in debug mode / Запуск додатку в режимі налагодження
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 