import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/звіт")
    markup.add(btn1)
    bot.send_message(message.chat.id, "Привіт! Я КІІТ-бот, готовий прийняти інвентаризацію!", reply_markup=markup)

@bot.message_handler(commands=["звіт"])
def start_report(message):
    text = """
*Пироги*

_З мʼясом:_
🍗🍅🧀 — Курка-томати-сир  
🍗🍄🧀 — Курка-гриби-сир  
🍗🍍 — Курка-ананас-сир  
🦃🫑 — Індик-солодкий перець  
🐄🧀 — Мʼясо-овочі  

_Без мʼяса:_
🧅 — Цибулевий  
🍄🧀 — Сир-гриби  
🧀🍃 — Сир-шпинат  
🧀 — Сім сирів  

_Солодкі:_
🍒🫐 — Вишня-чорниця  
🍒🧀 — Вишня-сир


*Пиріжки*

_Солоні:_
🥔 — Картопля  
🥔🍄 — Картопля-гриби  
🍄 — Гриби  
🥬 — Капуста  
🥬🥩 — Капуста-мʼясо  
🥩🥗 — Мʼясо-овочі  

_Солодкі:_
🍒 — Вишня  
🍒🍫 — Вишня-шоколад  
🍒🌼 — Вишня-мак  
🍐 — Груша  
(Слива)  
(Абрикос)  
(Вишня-крем)  
(Мак-крем)  
(Яблуко-кориця)


*Галети*
🥧🍏 — Яблуко-кориця  
🥧🍅 — Томати-сир

*Десерти*
🍰 Торт Наполеон  
🍯 Пахлава  
🥜 Горішки
"""
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

bot.polling()
