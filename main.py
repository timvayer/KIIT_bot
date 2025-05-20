import os
import telebot
import openai
from flask import Flask, request

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN is not set in environment variables.")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        print("===> Отримано повідомлення через webhook")
        bot.process_new_updates([update])
        return "", 200
    else:
        print("===> Отримано невірний тип контенту")
        return "Invalid content type", 403

@app.route("/", methods=["GET"])
def index():
    return "KIIT_bot з логуванням працює"

@bot.message_handler(commands=["start"])
def handle_start(message):
    print(f"===> /start від: {message.chat.id}")
    bot.send_message(message.chat.id, "Привіт! Напиши щось — я відповім як ChatGPT.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    print(f"===> Повідомлення від {message.chat.id}: {message.text}")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        reply = response.choices[0].message["content"].strip()
        print(f"===> Відповідь OpenAI: {reply}")
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        error_text = f"Сталася помилка: {e}"
        print("===>", error_text)
        bot.send_message(message.chat.id, error_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
