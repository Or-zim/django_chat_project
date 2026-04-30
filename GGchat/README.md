# Django Chat Project 

Простой чат на Django с использованием WebSockets (Channels), MySQL и Redis. Полностью упакован в Docker.

## Как запустить

1. Клонируйте репозиторий:
git clone https://github.com/Or-zim/django_chat_project.git

Потом перейдите в корневую папку:
cd django_chat_project/GGchat

3. Подготовьте настройки:
Скопируйте .env.example в .env:
cp .env.example .env

4. Запустите проект через Docker:
docker-compose up --build

5. Примените миграции:
docker-compose exec web python manage.py migrate

(дождитесь работы приложения, миграции применятся сами, в противном случае примените их сами)

7. Создайте суперпользователя:
docker-compose exec web python manage.py createsuperuser
(не обязательно)

9. Откройте проект:
Перейдите по адресу [localhost:8000](http://127.0.0.1:8000/accounts/index/)

Стек технологий
Python 3.10 / Django 5
Channels (WebSockets)
MySQL 8 (База данных)  
Daphne (ASGI сервер)
Docker / Docker-compose
Redis 7 (Channel Layer for WebSockets)
