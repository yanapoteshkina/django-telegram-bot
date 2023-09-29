pip install django

pip install djangorestframework

python manage.py makemigrations

python manage.py migrate 

python manage.py runserver 


в POSTMAN 

post - http://localhost:8000/users/register/

{
    "username": "root",
    "password": "root",
    "email": "test@gmail.com"
}

anserw: "user registered"


post -  http://localhost:8000/users/login/

{
    "username": "root",
    "password": "root"
}

anserw:

{
    "message": "Аутентификация успешна, ваш токен:",
    "token": "your_token_value"
}



post - http://localhost:8000/telegram-messages/create_message/

Перед созданием сообщений в headers postman надо указать "X-CSRFToken" со значением  csrftoken (можете получить в данных cookies после авторизации) в X-CSRFToken заголовке/ 

{
    "message_body": "Новое сообщение от Яны ! "
}



Для БОТА

pip install python-telegram-bot==13.15

pip install requests

python telegrambot.py