import os
import telebot
import openai
from flask import Flask, request

# Читання токенів з Environment Variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY
app = Flask(__name__)

# Обробка команди /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привіт! Я тут, слухаю тебе.")

# Обробка будь-якого іншого тексту
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}],
            temperature=0.7,
            max_tokens=500,
        )
        reply = response.choices[0].message.content.strip()
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, "Вибач, сталася помилка.")

# Webhook для Telegram
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "", 200
    else:
        return "Invalid content type", 403

# Головна сторінка
@app.route("/", methods=["GET"])
def index():
    return "KIIT_bot is live with ChatGPT integration!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
