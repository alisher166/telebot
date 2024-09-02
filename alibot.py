import telebot
from telebot import types
import json
import requests

# Ваш токен бота
TOKEN = '7202733857:AAGy9ZBPk2Pe2WFjI1g2MtISszozuy4mRHE'

# Функция для удаления вебхука
def delete_webhook(token):
    url = f'https://api.telegram.org/bot{token}/deleteWebhook'
    try:
        response = requests.post(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'Ошибка при удалении вебхука: {e}')
        return None

# Удаляем вебхук перед запуском бота
delete_response = delete_webhook(TOKEN)
print('Delete webhook response:', delete_response)

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_button = types.KeyboardButton(text='Открыть веб страницу', web_app=types.WebAppInfo(url='https://yourdomain.com/yourpage.html'))
    markup.add(web_button)
    bot.send_message(message.chat.id, 'Привет, мой друг!', reply_markup=markup)

# Обработчик данных с веб-страницы
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        res = json.loads(message.web_app_data.data)
        bot.send_message(message.chat.id, f'Name: {res["name"]}. Email: {res["email"]}. Phone: {res["phone"]}')
    except (json.JSONDecodeError, KeyError) as e:
        bot.send_message(message.chat.id, f'Ошибка обработки данных: {e}')

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)