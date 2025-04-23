from flask import Flask, request, jsonify
from flask_talisman import Talisman
from datetime import datetime
import logging
import re
from functools import wraps
import hashlib
import hmac
import os

app = Flask(__name__)

# Enable security headers / Увімкнення заголовків безпеки
Talisman(app,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'"
    },
    force_https=True
)

# Setup secure logging / Налаштування безпечного логування
logging.basicConfig(
    filename='payment.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def rate_limit(max_requests=100):
    """Rate limiting decorator / Декоратор обмеження частоти запитів"""
    requests = {}
    
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            now = datetime.now()
            ip = request.remote_addr
            
            # Clean old requests / Очищення старих запитів
            requests[ip] = [req for req in requests.get(ip, [])
                          if (now - req).total_seconds() < 3600]
            
            if len(requests.get(ip, [])) >= max_requests:
                return jsonify({"error": "Rate limit exceeded"}), 429
            
            requests.setdefault(ip, []).append(now)
            return f(*args, **kwargs)
        return wrapped
    return decorator

def validate_card_number(card_number):
    """Luhn algorithm for card validation / Алгоритм Луна для валідації карток"""
    if not re.match(r'^\d{16}$', card_number):
        return False
        
    digits = [int(d) for d in card_number]
    checksum = 0
    for i in range(len(digits)-1, -1, -1):
        d = digits[i]
        if i % 2 == 0:
            d = d * 2
            if d > 9:
                d = d - 9
        checksum += d
    return checksum % 10 == 0

def secure_card_storage(card_number):
    """Secure way to store card reference / Безпечний спосіб зберігання посилання на картку"""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        card_number.encode(),
        salt,
        100000
    )
    return hmac.new(key, card_number[-4:].encode(), hashlib.sha256).hexdigest()

# ❌ Vulnerable payment endpoint / Вразлива кінцева точка платежів
@app.route('/unsafe/process_payment', methods=['POST'])
def unsafe_process_payment():
    data = request.get_json()
    card_number = data.get('card_number')
    amount = data.get('amount')
    
    # UNSAFE: Logging sensitive data / НЕБЕЗПЕЧНО: Логування конфіденційних даних
    print(f"Processing payment: Card {card_number}, Amount: {amount}")
    
    # UNSAFE: No validation / НЕБЕЗПЕЧНО: Без валідації
    return jsonify({"status": "processed"})

# ✅ Secure payment endpoint / Безпечна кінцева точка платежів
@app.route('/secure/process_payment', methods=['POST'])
@rate_limit(max_requests=100)
def secure_process_payment():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), 400

        card_number = data.get('card_number')
        amount = data.get('amount')

        # Validate inputs / Валідація вхідних даних
        if not card_number or not amount:
            return jsonify({"error": "Missing required fields"}), 400
        
        if not validate_card_number(card_number):
            return jsonify({"error": "Invalid card number"}), 400

        if not isinstance(amount, (int, float)) or amount <= 0:
            return jsonify({"error": "Invalid amount"}), 400

        # Secure logging / Безпечне логування
        masked_card = f"****-****-****-{card_number[-4:]}"
        logging.info(f"Processing payment for card: {masked_card}")

        # Generate secure token for storage / Генерація безпечного токену для зберігання
        card_token = secure_card_storage(card_number)

        # Process payment here / Обробка платежу тут
        # ... payment processing code ...

        return jsonify({
            "status": "success",
            "transaction_id": os.urandom(8).hex(),
            "card_token": card_token
        })

    except Exception as e:
        logging.error(f"Payment processing error: {str(e)}")
        return jsonify({"error": "Payment processing failed"}), 500

if __name__ == '__main__':
    app.run(ssl_context='adhoc') 