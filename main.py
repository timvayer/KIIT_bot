
import telebot
import os
import flask
import logging
import json

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_TOKEN")

bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET'])
def index():
    return 'Bot is running.'

@app.route('/webhook', methods=['POST'])
def webhook():
    logging.info("===> Отримано повідомлення через webhook")
    json_string = flask.request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Привіт! Я працюю!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"Ти написав: {message.text}")

if __name__ == "__main__":
    app.run()
