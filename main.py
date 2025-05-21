import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Категорії виробів
pies_meat = {
    "🍗🍅🧀": "Курка-томати-сир",
    "🍗🍄🧀": "Курка-гриби-сир",
    "🍗🍍": "Курка-ананас-сир",
    "🦃🫑": "Індик-солодкий перець"
}
pies_veggie = {
    "🧅": "Цибулевий",
    "🍄🧀": "Сир-гриби",
    "🧀🍃": "Сир-шпинат",
    "🧀": "Сім сирів"
}
pies_sweet = {
    "🍒🫐": "Вишня-чорниця",
    "🍒🧀": "Вишня-сир"
}
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
galettes = {
    "🥧🍏": "Яблуко-кориця",
    "🥧🍅": "Томати-сир"
}
desserts = {
    "🍰": "Торт Наполеон",
    "🍯": "Пахлава",
    "🥜": "Горішки"
}

user_reports = {}

@bot.message_handler(commands=["start"])
def start_bot(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("/звіт", "/готово")
    bot.send_message(message.chat.id, "Привіт! Оберіть дію:", reply_markup=markup)

@bot.message_handler(commands=["звіт"])
def choose_category(message):
    chat_id = message.chat.id
    user_reports[chat_id] = []
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🥟 Пиріжки", callback_data="cat_pyrizhky"))
    markup.add(types.InlineKeyboardButton("🥧 Пироги", callback_data="cat_pies"))
    markup.add(types.InlineKeyboardButton("🍅 Галети", callback_data="cat_galettes"))
    markup.add(types.InlineKeyboardButton("🍰 Десерти", callback_data="cat_desserts"))
    bot.send_message(chat_id, "Що саме звітуємо?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("cat_"))
def handle_category(call):
    chat_id = call.message.chat.id
    markup = types.InlineKeyboardMarkup()
    category = call.data.split("_")[1]

    if category == "pyrizhky":
        for emoji, name in savory_pyrizhky.items():
            markup.add(types.InlineKeyboardButton(emoji, callback_data=f"item_{emoji}"))
        for emoji, name in sweet_pyrizhky.items():
            markup.add(types.InlineKeyboardButton(emoji, callback_data=f"item_{emoji}"))
    elif category == "pies":
        for emoji, name in pies_meat.items():
            markup.add(types.InlineKeyboardButton(emoji, callback_data=f"item_{emoji}"))
        for emoji, name in pies_veggie.items():
            markup.add(types.InlineKeyboardButton(emoji, callback_data=f"item_{emoji}"))
        for emoji, name in pies_sweet.items():
            markup.add(types.InlineKeyboardButton(emoji, callback_data=f"item_{emoji}"))
    elif category == "galettes":
        for emoji, name in galettes.items():
            markup.add(types.InlineKeyboardButton(emoji, callback_data=f"item_{emoji}"))
    elif category == "desserts":
        for emoji, name in desserts.items():
            markup.add(types.InlineKeyboardButton(emoji, callback_data=f"item_{emoji}"))

    bot.send_message(chat_id, "Оберіть виріб:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("item_"))
def ask_quantity(call):
    chat_id = call.message.chat.id
    emoji = call.data.split("_")[1]
    bot.send_message(chat_id, f"Скільки залишилось з {emoji}?")
    bot.register_next_step_handler(call.message, save_quantity, emoji)

def save_quantity(message, emoji):
    chat_id = message.chat.id
    qty = message.text.strip()
    if not qty.isdigit():
        bot.send_message(chat_id, "Будь ласка, введіть число.")
        return

    name = (
        savory_pyrizhky.get(emoji)
        or sweet_pyrizhky.get(emoji)
        or pies_meat.get(emoji)
        or pies_veggie.get(emoji)
        or pies_sweet.get(emoji)
        or galettes.get(emoji)
        or desserts.get(emoji)
        or "Невідомо"
    )

    user_reports[chat_id].append(f"{emoji} {name} — {qty} шт.")
    bot.send_message(chat_id, f"Записано: {emoji} {name} — {qty} шт.")

@bot.message_handler(commands=["готово"])
def show_report(message):
    chat_id = message.chat.id
    items = user_reports.get(chat_id, [])
    if not items:
        bot.send_message(chat_id, "Поки що нічого не заповнено.")
        return
    report = "\n".join(items)
    bot.send_message(chat_id, f"Готове:\n{report}")

bot.polling(none_stop=True)
