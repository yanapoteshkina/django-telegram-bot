import telegram
import requests
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler, CallbackContext
from telegram.ext import CallbackQueryHandler, JobQueue
import time


TOKEN_CODE = 'token BOT'

# URL для получения данных из первого API
API1_URL = 'http://localhost:8000/telegram-bot-token/'

# URL для получения данных из второго API
API2_BASE_URL = 'http://localhost:8000/telegram-messages/user_messages/'


TOKEN, AUTHENTICATED, WAITING_FOR_MESSAGE = range(3)

# Словарь для хранения данных пользователя
user_data = {}

# Словарь для хранения последних отправленных сообщений
last_sent_messages = {}

# Инициализация бота
bot = telegram.Bot(token=TOKEN_CODE)
updater = Updater(token=TOKEN_CODE, use_context=True)
dispatcher = updater.dispatcher

# Обработчик команды /start
def start(update, context):
    user_id = update.message.from_user.id
    bot.send_message(chat_id=update.message.chat_id, text="Введите свой токен:")
    return TOKEN

# Обработчик для получения и проверки токена
def get_token(update, context):
    user_id = update.message.from_user.id
    user_message = update.message.text

    # Запрашиваем токен пользователя из первого API
    response = requests.get(API1_URL)
    if response.status_code == 200:
        data = response.json()
        for item in data:
            if item.get('token') == user_message:
                user_to_lookup = item.get('user')
                user_data[user_id] = {'user_to_lookup': user_to_lookup, 'authenticated': True}
                bot.send_message(chat_id=update.message.chat_id, text="Вы аутентифицированы. \n\n Ожидайте сообщений \n\n Используйте команду /restart чтобы начать заново")
                # Начинаем отправку новых сообщений из API2 с таймером
                job_queue = updater.job_queue
                job_queue.run_repeating(check_api2_for_new_messages, interval=5, first=0, context=update)
                return AUTHENTICATED

    bot.send_message(chat_id=update.message.chat_id, text="Токен не найден. Попробуйте еще раз. ")
    return TOKEN

# Обработчик команды /restart
def restart(update, context):
    user_id = update.message.from_user.id
    user_data[user_id] = {'authenticated': False}
    bot.send_message(chat_id=update.message.chat_id, text="Введите свой токен:")
    return TOKEN

# Функция для проверки и отправки новых сообщений из API2
def check_api2_for_new_messages(context: CallbackContext):
    job = context.job
    user_id = job.context.message.from_user.id

    if user_data.get(user_id, {}).get('authenticated', False):
        user_to_lookup = user_data[user_id]['user_to_lookup']

        # Формируем URL для второго API с параметром user_id
        api2_url = f'{API2_BASE_URL}?user_id={user_to_lookup}'
        # Отправляем запрос на второе API
        response = requests.get(api2_url)
        if response.status_code == 200:
            data = response.json()
            if data:
                latest_message = data[-1].get('message_body', 'Нет сообщения')
                user_name = context.job.context.message.from_user.first_name
                response_text = f'{user_name}, я получил от тебя сообщение: {latest_message}'

                # Проверяем, было ли отправлено это сообщение ранее
                if last_sent_messages.get(user_id) != latest_message:
                    bot.send_message(chat_id=context.job.context.message.chat_id, text=response_text)
                    last_sent_messages[user_id] = latest_message
            else:
                pass

# Создаем конечный автомат
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        TOKEN: [MessageHandler(Filters.text & ~Filters.command, get_token)],
        AUTHENTICATED: [
            CommandHandler('restart', restart),
        ],
    },
    fallbacks=[],
)
dispatcher.add_handler(conv_handler)

# Запускаем бота
updater.start_polling()
updater.idle()
