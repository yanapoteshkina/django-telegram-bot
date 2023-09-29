DJANGO 

перейдите в django_tg


Зависисмости:

pip install django

pip install djangorestframework

python manage.py makemigrations

python manage.py migrate 

python manage.py runserver 


-----


в POSTMAN

Регистрация пользователя

POST - http://localhost:8000/users/register/


body:

{
    "username": "root",
    "password": "root",
    "email": "test@gmail.com"
}

well anserw: "user registered"



Аутентификация пользователя и получение персонального токена

POST -  http://localhost:8000/users/login/


body:

{
    "username": "root",
    "password": "root"
}

well anserw:

{
    "message": "Аутентификация успешна, ваш токен:",
    "token": "your_token_value"
}


Создание сообщения от пользователя

POST - http://localhost:8000/telegram-messages/create_message/

Перед созданием сообщений в headers postman надо указать строчку "X-CSRFToken" со значением  csrftoken (можете получить в данных cookies после авторизации)

{
    "message_body": "Новое сообщение от Яны ! "
}


-----



ЧАТ БОТ ТЕЛЕГРАМ 

перейдите в telegrambot.py


Зависисмости:

pip install python-telegram-bot==13.15

pip install requests

python telegrambot.py

---

Установите Токен в переменной - TOKEN_CODE

