import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

user_reports = {}
user_stage = {}
user_category = {}
user_subcategory = {}

# Дані
pies = {
    "Пиріжки": {
        "Солоні": {
            "🥔": "Картопля",
            "🥔🍄": "Картопля-гриби",
            "🍄": "Гриби",
            "🥬": "Капуста",
            "🥬🥩": "Капуста-мʼясо",
            "🥩🥗": "Мʼясо-овочі"
        },
        "Солодкі": {
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
    },
    "Пироги": {
        "З мʼясом": {
            "🍗🍅🧀": "Курка-томати-сир",
            "🍗🍄🧀": "Курка-гриби-сир",
            "🦃🫑": "Індик-перець",
        },
        "Без мʼяса": {
            "🧅": "Цибулевий",
            "🧀🍄": "Сир-гриби",
            "🧀🥬": "Сир-шпинат",
            "🧀": "Сім сирів"
        },
        "Солодкі": {
            "🍒🔵": "Вишня-чорниця",
            "🍒🧀": "Вишня-сир"
        }
    },
    "Галети": {
        "🥧🍏": "Яблуко-кориця",
        "🥧🍅": "Томати-сир"
    },
    "Десерти": {
        "🍰": "Торт Наполеон",
        "🍯": "Пахлава",
        "🥜": "Горішки"
    }
}

# Команда /start або /звіт
@bot.message_handler(commands=["start", "звіт"])
def start_report(message):
    chat_id = message.chat.id
    user_reports[chat_id] = []
    user_stage[chat_id] = "category"
    markup = types.InlineKeyboardMarkup()
    for cat in pies:
        markup.add(types.InlineKeyboardButton(f"{list(pies[cat].values())[0] if isinstance(pies[cat], dict) else ''} {cat}", callback_data=cat))
    bot.send_message(chat_id, "Оберіть категорію:", reply_markup=markup)

# Обробка кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    data = call.data

    if user_stage.get(chat_id) == "category":
        user_category[chat_id] = data
        if isinstance(pies[data], dict) and all(isinstance(v, dict) for v in pies[data].values()):
            user_stage[chat_id] = "subcategory"
            markup = types.InlineKeyboardMarkup()
            for subcat in pies[data]:
                markup.add(types.InlineKeyboardButton(subcat, callback_data=subcat))
            bot.send_message(chat_id, "Оберіть підкатегорію:", reply_markup=markup)
        else:
            user_stage[chat_id] = "product"
            show_products(chat_id, pies[data])
    elif user_stage.get(chat_id) == "subcategory":
        user_subcategory[chat_id] = data
        user_stage[chat_id] = "product"
        category = user_category[chat_id]
        show_products(chat_id, pies[category][data])
    elif user_stage.get(chat_id) == "product":
        emoji = data
        category = user_category[chat_id]
        subcat = user_subcategory.get(chat_id)
        name = pies[category][subcat][emoji] if subcat else pies[category][emoji]
        user_stage[chat_id] = "quantity"
        user_reports[chat_id].append({"emoji": emoji, "name": name})
        bot.send_message(chat_id, f"Скільки залишилось з {emoji}?")

# Введення кількості
@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_quantity(message):
    chat_id = message.chat.id
    if user_stage.get(chat_id) == "quantity":
        qty = int(message.text)
        if user_reports.get(chat_id):
            user_reports[chat_id][-1]["qty"] = qty
            last = user_reports[chat_id][-1]
            bot.send_message(chat_id, f"Записано: {last['emoji']} {last['name']} — {qty} шт.")
        user_stage[chat_id] = "product"
        # Повторне виведення продуктів
        category = user_category[chat_id]
        subcat = user_subcategory.get(chat_id)
        current_dict = pies[category][subcat] if subcat else pies[category]
        show_products(chat_id, current_dict)

# /готово — фінал
@bot.message_handler(commands=["готово"])
def finish_report(message):
    chat_id = message.chat.id
    if chat_id in user_reports:
        text = "*Готове:*\n"
        for item in user_reports[chat_id]:
            text += f"{item['emoji']} {item['name']} — {item['qty']} шт.\n"
        bot.send_message(chat_id, text, parse_mode="Markdown")
        del user_reports[chat_id]
        user_stage[chat_id] = None

# Допоміжна
def show_products(chat_id, items_dict):
    markup = types.InlineKeyboardMarkup()
    row = []
    for i, emoji in enumerate(items_dict):
        btn = types.InlineKeyboardButton(emoji, callback_data=emoji)
        row.append(btn)
        if len(row) == 2:
            markup.add(*row)
            row = []
    if row:
        markup.add(*row)
    bot.send_message(chat_id, "Оберіть виріб:", reply_markup=markup)

bot.polling()
