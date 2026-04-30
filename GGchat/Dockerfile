# Используем стабильный Python
FROM python:3.10-slim

# Запрещаем Python писать файлы .pyc и включаем буферизацию логов
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Устанавливаем системные зависимости для MySQL и сборки пакетов
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . /app/

# Открываем порт
EXPOSE 8000

# Запуск через Daphne (так как у нас Channels/Чат)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "GGchat.asgi:application"]