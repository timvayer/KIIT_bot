import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# --- Дані ---
pies = {
    "🥧 Пироги": {
        "З м’ясом": {
            "🍗🍅🧀": "Курка-томати-сир",
            "🍗🍄🧀": "Курка-гриби-сир",
            "🍗🍍": "Курка-ананас-сир",
            "🦃🫑": "Індик-солодкий перець",
            "🐄🧀": "Телятина-сир"
        },
        "Без м’яса": {
            "🧅": "Цибулевий",
            "🧀🍃": "Сир-шпинат",
            "🍄🧀": "Гриби-сир",
            "🧀": "Сім сирів"
        },
        "Солодкі": {
            "🍒🫐": "Вишня-лохина",
            "🍒🧀": "Вишня-сир"
        }
    },
    "🥟 Пиріжки": {
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
    "🍅 Галети": {
        "🥧🍏": "Яблуко-кориця",
        "🥧🍅": "Томати-сир"
    },
    "🍰 Десерти": {
        "🍰": "Торт Наполеон",
        "🍯": "Пахлава",
        "🥜": "Горішки"
    }
}

user_state = {}
user_reports = {}

# --- Команди ---
@bot.message_handler(commands=["start", "звіт"])
def start_report(message):
    chat_id = message.chat.id
    user_state[chat_id] = {"stage": "category"}
    user_reports[chat_id] = []
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for category in pies:
        markup.add(types.KeyboardButton(category))
    markup.add(types.KeyboardButton("Скасувати"))
    bot.send_message(chat_id, "Що саме звітуємо?", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in pies)
def select_category(message):
    chat_id = message.chat.id
    user_state[chat_id]["category"] = message.text
    subcats = pies[message.text]
    if isinstance(subcats, dict) and all(isinstance(v, dict) for v in subcats.values()):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for subcat in subcats:
            markup.add(types.KeyboardButton(subcat))
        markup.add(types.KeyboardButton("↩ Назад до категорій"))
        user_state[chat_id]["stage"] = "subcategory"
        bot.send_message(chat_id, f"Оберіть підкатегорію {message.text.lower()}:", reply_markup=markup)
    else:
        user_state[chat_id]["stage"] = "product"
        show_products(chat_id, subcats)

@bot.message_handler(func=lambda m: m.text == "↩ Назад до категорій")
def back_to_categories(message):
    start_report(message)

@bot.message_handler(func=lambda m: m.text in ["З м’ясом", "Без м’яса", "Солодкі", "Солоні"])
def select_subcategory(message):
    chat_id = message.chat.id
    category = user_state[chat_id]["category"]
    subcat = message.text
    user_state[chat_id]["subcategory"] = subcat
    products = pies[category][subcat]
    user_state[chat_id]["stage"] = "product"
    show_products(chat_id, products)

def show_products(chat_id, products_dict):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for emoji in products_dict:
        markup.add(types.KeyboardButton(emoji))
    markup.add(types.KeyboardButton("↩ Назад до категорій"), types.KeyboardButton("✅ Готово"))
    user_state[chat_id]["products"] = products_dict
    bot.send_message(chat_id, "Оберіть виріб:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "✅ Готово")
def done(message):
    chat_id = message.chat.id
    entries = user_reports.get(chat_id, [])
    if not entries:
        bot.send_message(chat_id, "Поки що нічого не збережено.")
    else:
        text = "*Готове:*\n" + "\n".join([f"{emoji} {name} — {qty} шт." for emoji, name, qty in entries])
        bot.send_message(chat_id, text, parse_mode="Markdown")
    user_state.pop(chat_id, None)
    user_reports.pop(chat_id, None)

@bot.message_handler(func=lambda m: m.text in sum([list(v.values()) if isinstance(v, dict) else [] for c in pies.values() for v in (c.values() if isinstance(c, dict) else [c])], []))
def fallback(message):
    bot.send_message(message.chat.id, "Будь ласка, натисніть кнопку.")

@bot.message_handler(func=lambda m: m.text in sum([list(d.keys()) for d in pies.values() if isinstance(d, dict)], []))
def select_item(message):
    chat_id = message.chat.id
    emoji = message.text
    name = user_state[chat_id]["products"][emoji]
    user_state[chat_id]["selected"] = (emoji, name)
    bot.send_message(chat_id, f"Скільки залишилось з {emoji}?")

@bot.message_handler(func=lambda m: m.text.isdigit())
def save_quantity(message):
    chat_id = message.chat.id
    emoji, name = user_state[chat_id].get("selected", (None, None))
    qty = int(message.text)
    if emoji:
        user_reports[chat_id].append((emoji, name, qty))
        bot.send_message(chat_id, f"Записано: {emoji} {name} — {qty} шт.")
    category = user_state[chat_id]["category"]
    stage = user_state[chat_id]["stage"]
    if stage == "product":
        if "subcategory" in user_state[chat_id]:
            subcat = user_state[chat_id]["subcategory"]
            show_products(chat_id, pies[category][subcat])
        else:
            show_products(chat_id, pies[category])
