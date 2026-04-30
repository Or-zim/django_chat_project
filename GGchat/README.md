# Django Chat Project 

Простой чат на Django с использованием WebSockets (Channels), MySQL и Redis. Полностью упакован в Docker.

## Как запустить

1. Клонируйте репозиторий:
   git clone https://github.com/Or-zim/django_chat_project.git
   cd django_chat_project/GGchat

2. Подготовьте настройки:
Скопируйте .env.example в .env:
cp .env.example .env

3. Запустите проект через Docker:
docker-compose up --build

4. Примените миграции:
docker-compose exec web python manage.py migrate

5. Создайте суперпользователя:
docker-compose exec web python manage.py createsuperuser

6. Откройте проект:
Перейдите по адресу http://localhost:8000

Стек технологий
Python 3.10 / Django 5
Channels (WebSockets)
MySQL 8 (База данных)
Daphne (ASGI сервер)
Docker / Docker-compose
Redis 7 (Channel Layer for WebSockets)