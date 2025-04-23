# Security Guidelines and Demonstrations
## Рекомендації з безпеки та демонстрації

### 1. Common Security Vulnerabilities / Поширені вразливості безпеки

#### 1.1 Credit Card Data Interception / Перехоплення даних кредитної картки
```python
# ❌ Unsafe way / Небезпечний спосіб
@app.route('/process_payment', methods=['POST'])
def unsafe_process_payment():
    card_number = request.form['card_number']  # Plain text in logs
    print(f"Processing payment for card: {card_number}")  # Logging sensitive data
    return "Payment processed"

# ✅ Secure way / Безпечний спосіб
@app.route('/process_payment', methods=['POST'])
def secure_process_payment():
    card_number = request.form['card_number']
    masked_number = f"****-****-****-{card_number[-4:]}"
    logging.info(f"Processing payment for card: {masked_number}")
    return "Payment processed"
```

#### 1.2 SQL Injection Prevention / Запобігання SQL-ін'єкціям
```python
# ❌ Vulnerable to SQL injection / Вразливий до SQL-ін'єкції
@app.route('/user/<username>')
def unsafe_get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)  # DANGEROUS!

# ✅ Safe from SQL injection / Захищений від SQL-ін'єкції
@app.route('/user/<username>')
def safe_get_user(username):
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
```

### 2. Docker Security Best Practices / Найкращі практики безпеки Docker

#### 2.1 Secure Dockerfile Example / Приклад безпечного Dockerfile
```dockerfile
# Use specific version tags
FROM python:3.9-slim

# Run as non-root user
RUN useradd -m appuser
USER appuser

# Minimize attack surface
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Use environment variables for secrets
ENV SECRET_KEY_FILE=/run/secrets/secret_key
```

#### 2.2 Docker-compose Security / Безпека Docker-compose
```yaml
services:
  web:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    secrets:
      - secret_key
```

### 3. Flask Security Headers / Заголовки безпеки Flask

```python
from flask_talisman import Talisman

# Enable security headers
Talisman(app,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'"
    },
    force_https=True
)
```

### 4. Demonstration: Credit Card Data Protection / Демонстрація: Захист даних кредитних карток

See the example implementation in `secure_payment_demo.py` showing:
- Data encryption in transit
- Secure logging practices
- Input validation
- PCI DSS compliance basics

### 5. Security Checklist / Контрольний список безпеки

1. ✅ Use HTTPS / Використовуйте HTTPS
2. ✅ Implement rate limiting / Впровадьте обмеження частоти запитів
3. ✅ Validate all inputs / Перевіряйте всі вхідні дані
4. ✅ Use secure headers / Використовуйте безпечні заголовки
5. ✅ Keep dependencies updated / Оновлюйте залежності
6. ✅ Use secure session configuration / Використовуйте безпечну конфігурацію сесій
7. ✅ Implement proper authentication / Впровадьте належну автентифікацію
8. ✅ Use secure password hashing / Використовуйте безпечне хешування паролів 