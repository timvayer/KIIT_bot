import telebot
import os
from flask import Flask, request

TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'KIIT_bot is running', 200

@app.route('/', methods=['POST'])
def receive_update():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return '', 200

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привіт! Я працюю.")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, f"Ти сказав: {message.text}")
