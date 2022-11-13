# praktikum_new_diplom
# «Продуктовый помощник» - Foodgram
Foodgram  - cервис позволяющий создавать рецепты, подписываться на других пользователей, добавлять понравившиеся рецепты в список избранное, скачивать список продуктов для приготовления.

## Список используемых библиотек и фреймворков:
* gunicorn==20.0.4
* psycopg2-binary==2.8.6
* requests==2.26.0
* django==2.2.16
* djangorestframework==3.12.4
* PyJWT==2.1.0
* pytest==6.2.4
* pytest-django==4.4.0
* pytest-pythonpath==0.7.3
* djangorestframework-simplejwt==4.7.2
* django-filter==21.1
* djoser==2.1.0
* drf-base64==2.0
* drf-extra-fields==3.4.0
* pytz==2020.1
* sqlparse==0.3.1


## шаблон наполнения env-файла:
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=имя базы данных
POSTGRES_USER=логин для подключения к базе данных
POSTGRES_PASSWORD=пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY=ваш SECRET_KEY из settings.py
```

## Команды для запуска проекта:

1. Соберите контейнеры и запустите их
```
docker-compose up -d --build
```
2. Выполните по очереди команды:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec web python manage.py load_data
```

3. Для остановки контейнеров выполние команду:
```
docker-compose stop
```
---
## Разработчик:
- [Александр Шарганов](https://github.com/AlexandrSharganov)


![deploy status](https://github.com/AlexandrSharganov/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
