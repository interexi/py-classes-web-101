# Use Python official image / Використовуємо офіційний образ Python
FROM python:3.9-slim

# Set working directory / Встановлюємо робочу директорію
WORKDIR /app

# Copy requirements first for better caching / Спочатку копіюємо requirements для кращого кешування
COPY requirements.txt .

# Install dependencies / Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code / Копіюємо код додатку
COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

# Set environment variables / Встановлюємо змінні середовища
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port / Відкриваємо порт
EXPOSE 5000

# Run the application / Запускаємо додаток
CMD ["flask", "run", "--host=0.0.0.0"] 