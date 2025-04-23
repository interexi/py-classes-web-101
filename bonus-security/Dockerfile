# Use specific version for security / Використовуємо конкретну версію для безпеки
FROM python:3.9-slim-bullseye

# Create non-root user / Створюємо користувача без прав root
RUN useradd -m -s /bin/bash appuser

# Set working directory / Встановлюємо робочу директорію
WORKDIR /app

# Install security updates and dependencies / Встановлюємо оновлення безпеки та залежності
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        gcc \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first / Спочатку копіюємо requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code / Копіюємо код додатку
COPY secure_payment_demo.py .

# Set proper permissions / Встановлюємо правильні права доступу
RUN chown -R appuser:appuser /app && \
    chmod -R 500 /app

# Switch to non-root user / Перемикаємося на користувача без прав root
USER appuser

# Set secure environment / Встановлюємо безпечне середовище
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Use non-privileged port / Використовуємо непривілейований порт
EXPOSE 8080

# Run with secure settings / Запускаємо з безпечними налаштуваннями
CMD ["python", "secure_payment_demo.py"] 