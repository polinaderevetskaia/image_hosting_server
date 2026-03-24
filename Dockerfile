FROM python:3.12-slim
#базовий образ з Python 3.12

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
#оновлюємо пакети та встановлюємо додаткові
#компилятор C
#клієнт для роботи з PostgreSQL
#очищаємо кеш для зменшення розміру образу

RUN useradd --create-home --shell /bin/bash appuser
#створюємо користувача appuser

RUN mkdir -p /images && chown appuser:appuser /images
#створюємо директорію для зображень і даємо права користувачу

COPY requirements.txt .
#копіюємо файл залежностей у контейнер
RUN pip install --no-cache-dir -r requirements.txt
#встановлюємо Python-залежності без кешу

COPY src/ /app/src/
#копіюємо вихідний код додатку в контейнер

RUN chown -R appuser:appuser /app
#встановлюємо власника директорії /app на appuser

USER appuser
#виконуємо всі подальші команди від імені appuser
WORKDIR /app
#встановлюємо робочу директорію для запуску команд

EXPOSE 8000
#відкриваємо порт 8000 для зовнішнього доступу

CMD ["python", "src/app.py"]
#команда запуску додатку при старті контейнера
