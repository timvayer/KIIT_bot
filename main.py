import os
import telebot
from flask import Flask, request

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

print("=== TELEGRAM_TOKEN from ENV ===")
print(TELEGRAM_TOKEN)

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found in environment variables")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "KIIT echo-bot is running!"

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == '__main__':
    app.run(debug=True)
