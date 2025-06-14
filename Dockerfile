FROM python:3.11-slim

# Установка Poetry
RUN pip install --no-cache-dir poetry==2.1.3

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем
COPY back/pyproject.toml back/poetry.lock* /app/
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

# Копируем остальной код
COPY back /app

# Открываем порт
EXPOSE 8080

# Запуск
CMD ["python", "app.py"]
