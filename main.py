
import telebot
from telebot import types
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Список пирогів з емодзі
pies = {
    "🍗🍍": "Курка-ананас-сир",
    "🍗🍄🧀": "Курка-гриби-сир",
    "🍗🍅🧀": "Курка-томати-сир",
    "🐄🧀": "Мʼясо-овочі",
    "🦃🫑": "Індик-солодкий перець",
    "🧅": "Цибулевий",
    "🧀🍃": "Сир-шпинат",
    "🍄🧀": "Сир-гриби",
    "🧀": "Сім сирів",
    "🍒🫐": "Вишня-чорниця",
    "🍒🧀": "Вишня-сир"
}

@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/звіт")
    markup.add(btn1)
    bot.send_message(message.chat.id, "Привіт! Я працюю!", reply_markup=markup)

@bot.message_handler(commands=["звіт"])
def start_report(message):
    markup = types.InlineKeyboardMarkup()
    btn_pies = types.InlineKeyboardButton("🥧 Пироги", callback_data="category_pies")
    markup.add(btn_pies)
    bot.send_message(message.chat.id, "Оберіть категорію:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "category_pies")
def show_pies(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for emoji, name in pies.items():
        markup.add(types.InlineKeyboardButton(text=emoji, callback_data=f"pie_{emoji}"))
    bot.edit_message_text("Оберіть пиріг:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("pie_"))
def ask_quantity(call):
    pie_emoji = call.data.split("_", 1)[1]
    pie_name = pies.get(pie_emoji, "Пиріг")
    msg = bot.send_message(call.message.chat.id, f"Скільки шматків залишилось для {pie_name}?")
    bot.register_next_step_handler(msg, lambda m: confirm_quantity(m, pie_emoji, pie_name))

def confirm_quantity(message, pie_emoji, pie_name):
    bot.send_message(message.chat.id, f"Записано: {pie_name} {pie_emoji} — {message.text} шт.")

bot.polling()
