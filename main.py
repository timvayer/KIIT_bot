
import logging
import openai
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters

# Токен Telegram-бота
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
# API-ключ OpenAI
OPENAI_API_KEY = "your_openai_api_key"

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
bot = telegram.Bot(token=TELEGRAM_TOKEN)

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

def handle_message(update, context):
    user_text = update.message.text
    chat_id = update.message.chat_id

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ти — персональний помічник кавʼярні КІІТ, говориш українською, відповідаєш чітко, по суті, з теплом."},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7
        )
        reply_text = response.choices[0].message.content
    except Exception as e:
        reply_text = f"Помилка: {e}"

    bot.send_message(chat_id=chat_id, text=reply_text)

dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

@app.route("/")
def index():
    return "Бот КІІТ працює!"

if __name__ == "__main__":
    app.run(port=8443)
