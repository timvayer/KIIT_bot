import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Дані
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

meat_pies = {
    "🍗🍅🧀": "Курка-томати-сир",
    "🍗🍄🧀": "Курка-гриби-сир",
    "🍗🍍": "Курка-ананас-сир",
    "🦃🫑": "Індик-солодкий перець"
}
veggie_pies = {
    "🧅": "Цибулевий",
    "🍄🧀": "Сир-гриби",
    "🧀🍃": "Сир-шпинат",
    "🧀": "Сім сирів"
}
sweet_pies = {
    "🍒🫐": "Вишня-чорниця",
    "🍒🧀": "Вишня-сир"
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

    structure_text = """*Пироги*

_З мʼясом:_
🍗🍅🧀 — Курка-томати-сир
🍗🍄🧀 — Курка-гриби-сир
🍗🍍 — Курка-ананас-сир
🦃🫑 — Індик-солодкий перець

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
Слива — Слива
Абрикос — Абрикос
Вишня-крем — Вишня-крем
Мак-крем — Мак-крем
Яблуко-кориця — Яблуко-кориця
"""
    bot.send_message(chat_id, structure_text, parse_mode="Markdown")

    markup = types.InlineKeyboardMarkup(row_width=3)
    for emoji in (
        list(meat_pies.keys()) + list(veggie_pies.keys()) + list(sweet_pies.keys()) +
        list(savory_pyrizhky.keys()) + list(sweet_pyrizhky.keys())
    ):
        markup.add(types.InlineKeyboardButton(emoji, callback_data=f"item_{emoji}"))
    bot.send_message(chat_id, "Оберіть виріб:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("item_"))
def ask_quantity(call):
    chat_id = call.message.chat.id
    emoji = call.data.split("_", 1)[1]
    name = (
        meat_pies.get(emoji)
        or veggie_pies.get(emoji)
        or sweet_pies.get(emoji)
        or savory_pyrizhky.get(emoji)
        or sweet_pyrizhky.get(emoji)
        or "невідомий"
    )
    msg = bot.send_message(chat_id, f"Скільки залишилось з {emoji}?")
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
