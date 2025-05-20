
import os
import telebot
import openai
from flask import Flask, request

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if TELEGRAM_TOKEN is None:
    raise ValueError("TELEGRAM_TOKEN is not set in environment variables.")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid content type', 403

@app.route('/', methods=['GET'])
def index():
    return 'KIIT Bot is running.'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привіт! Напиши мені щось, і я відповім як ChatGPT.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_message = message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти — доброзичливий Telegram-бот кавʼярні КІІТ."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message['content'].strip()
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
