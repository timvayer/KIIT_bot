
import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Список пиріжків (тільки для інтерактиву поки що)
savory_pyrizhky = {
    "🥔": "Картопля",
    "🥔🍄": "Картопля-гриби",
    "🍄": "Гриби",
    "🥬": "Капуста",
    "🥬🥩": "Капуста-мʼясо",
    "🥩🥗": "Мʼясо-овочі"
}

sweet_pyrizhky = {
    "🍒": "Вишня",
    "🍒🍫": "Вишня-шоколад",
    "🍒🌼": "Вишня-мак",
    "🍐": "Груша",
    "Слива": "Слива",
    "Абрикос": "Абрикос",
    "Вишня-крем": "Вишня-крем",
    "Мак-крем": "Мак-крем",
    "Яблуко-кориця": "Яблуко-кориця"
}

user_reports = {}

@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/звіт"), types.KeyboardButton("/готово"))
    bot.send_message(message.chat.id, "Привіт! Я КІІТ-бот, готовий прийняти інвентаризацію!", reply_markup=markup)

@bot.message_handler(commands=["звіт"])
def start_report(message):
    chat_id = message.chat.id
    user_reports[chat_id] = []

    # Виводимо повну структуру
    text = "*Пиріжки*

_Солоні:_\n"
    for emoji, name in savory_pyrizhky.items():
        text += f"{emoji} — {name}\n"

    text += "\n_Солодкі:_\n"
    for emoji, name in sweet_pyrizhky.items():
        text += f"{emoji} — {name}\n"

    bot.send_message(chat_id, text, parse_mode="Markdown")

    # Показуємо кнопки лише для пиріжків
    markup = types.InlineKeyboardMarkup(row_width=2)
    for emoji in list(savory_pyrizhky.keys()) + list(sweet_pyrizhky.keys()):
        markup.add(types.InlineKeyboardButton(emoji, callback_data=f"pyrizhok_{emoji}"))
    bot.send_message(chat_id, "Оберіть пиріжок:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("pyrizhok_"))
def ask_quantity(call):
    chat_id = call.message.chat.id
    emoji = call.data.split("_", 1)[1]
    name = savory_pyrizhky.get(emoji) or sweet_pyrizhky.get(emoji) or "невідомий"
    msg = bot.send_message(chat_id, f"Скільки залишилось пиріжків з {emoji}?")
    bot.register_next_step_handler(msg, lambda m: save_quantity(m, emoji, name))

def save_quantity(message, emoji, name):
    chat_id = message.chat.id
    qty = message.text.strip()
    if chat_id not in user_reports:
        user_reports[chat_id] = []
    user_reports[chat_id].append(f"{emoji} {name} — {qty} шт.")

    bot.send_message(chat_id, f"Записано: {emoji} {name} — {qty} шт.")

@bot.message_handler(commands=["готово"])
def finish_report(message):
    chat_id = message.chat.id
    data = user_reports.get(chat_id, [])
    if not data:
        bot.send_message(chat_id, "Нічого не внесено.")
        return

    final_text = "*Готове:*\n" + "\n".join(data)
    bot.send_message(chat_id, final_text, parse_mode="Markdown")

bot.polling()
