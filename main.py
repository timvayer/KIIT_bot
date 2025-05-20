
import os
import logging
from flask import Flask, request
import telebot

# Увімкнення логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація Flask і TeleBot
app = Flask(__name__)
bot = telebot.TeleBot(os.environ.get("TELEGRAM_TOKEN"))

@app.route('/', methods=['GET'])
def index():
    return 'Bot is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        json_string = request.get_data().decode('utf-8')
        logger.info("===> Отримано повідомлення через webhook: %s", json_string)
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
    except Exception as e:
        logger.exception("Помилка обробки webhook: %s", e)
    return '', 200

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        logger.info("===> Повідомлення від користувача: %s", message.text)
        bot.reply_to(message, f"Ви написали: {message.text}")
    except Exception as e:
        logger.exception("Не вдалося відповісти: %s", e)

if __name__ == "__main__":
    app.run(debug=True)
