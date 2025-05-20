import os
import telebot
import openai
from flask import Flask, request

# Зчитуємо ключі з environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ініціалізація ботів
bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "", 200
    else:
        return "Invalid content type", 403

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Привіт! Я інтегрований з ChatGPT. Напиши щось.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Відповідай коротко, українською мовою, дружньо і з гумором."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, f"Сталася помилка: {e}")

@app.route("/", methods=["GET"])
def index():
    return "KIIT_bot with ChatGPT is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)