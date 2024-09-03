import telebot
from telebot import types
import json
import requests

# Ваш токен бота
TOKEN = '7202733857:AAGy9ZBPk2Pe2WFjI1g2MtISszozuy4mRHE'  # Не забудьте заменить на свой токен

# Функция для удаления вебхука перед запуском бота
def delete_webhook(token):
    url = f'https://api.telegram.org/bot{token}/deleteWebhook'
    try:
        response = requests.post(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'Ошибка при удалении вебхука: {e}')
        return None

delete_response = delete_webhook(TOKEN)
print('Delete webhook response:', delete_response)

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Вставьте ваш реальный URL сюда
    web_button = types.KeyboardButton(text='Открыть веб страницу', web_app=types.WebAppInfo(url='https://alisher166.github.io/telebot/'))
    markup.add(web_button)
    bot.send_message(message.chat.id, 'Привет! Оформите заказ через веб-страницу.', reply_markup=markup)

# Обработчик данных с веб-страницы
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        # Получаем данные, отправленные из веб-приложения
        data = json.loads(message.web_app_data.data)
        response_text = f"Имя: {data.get('name', 'Не указано')}\nEmail: {data.get('email', 'Не указано')}\nТелефон: {data.get('phone', 'Не указано')}"
        bot.send_message(message.chat.id, response_text)
    except (json.JSONDecodeError, KeyError) as e:
        bot.send_message(message.chat.id, f'Ошибка обработки данных: {e}')

if __name__ == '__main__':
    bot.polling(none_stop=True)


