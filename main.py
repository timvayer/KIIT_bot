
import os
import logging
from flask import Flask, request
from telebot import TeleBot, types

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація Flask і TeleBot
app = Flask(__name__)
bot = TeleBot(os.environ.get("TELEGRAM_TOKEN"))

@app.route('/webhook', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    logger.info("====> Отримано повідомлення через webhook: %s", json_string)
    update = types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

# Реакція на команду /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привіт! Я працюю.")

# Реакція на будь-яке інше повідомлення
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"Ти сказав: {message.text}")

# Запуск (не потрібно при використанні webhook)
if __name__ == '__main__':
    app.run()
