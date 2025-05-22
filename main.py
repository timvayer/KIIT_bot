import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

user_reports = {}
user_states = {}

# === КАТЕГОРІЇ ===
categories = ["Пироги", "Пиріжки", "Галети", "Десерти"]

# === ПИРОГИ ===
pies = {
    "З мʼясом": {
        "🍗🍅🧀": "Курка-томати-сир",
        "🍗🍍🧀": "Курка-ананас-сир",
        "🍗🍄🧀": "Курка-гриби-сир",
        "🐄🧀": "Телятина-сир",
        "🦃🫑": "Індик-солодкий перець"
    },
    "Без мʼяса": {
        "🧅": "Цибулевий",
        "🍄🧀": "Гриби-сир",
        "🧀🍃": "Сир-шпинат",
        "🧀": "Сім сирів"
    },
    "Солодкі": {
        "🍒🫐": "Вишня-лохина",
        "🍒🧀": "Вишня-сир"
    }
}

# === ПИРІЖКИ ===
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

# === ГАЛЕТИ І ДЕСЕРТИ ===
galety = {"🥧🍏": "Яблуко-кориця", "🥧🍅": "Томати-сир"}
deserty = {"🍰": "Торт Наполеон", "🍯": "Пахлава", "🥜": "Горішки"}

# === СТАРТ / ЗВІТ ===
@bot.message_handler(commands=["start", "звіт"])
def start_report(message):
    chat_id = message.chat.id
    user_reports[chat_id] = []
    user_states[chat_id] = {"stage": "category"}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for cat in categories:
        markup.add(cat)
    markup.add("Скасувати")
    bot.send_message(chat_id, "Що саме звітуємо?", reply_markup=markup)

# === ОБРОБКА ВИБОРУ ===
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    chat_id = message.chat.id
    text = message.text
    state = user_states.get(chat_id, {"stage": "category"})

    if text == "Скасувати":
        bot.send_message(chat_id, "Звіт скасовано.")
        user_states.pop(chat_id, None)
        return

    if text == "/готово":
        result = "\n".join(user_reports.get(chat_id, []) or ["(нічого не збережено)"])
        bot.send_message(chat_id, f"*Готове:*\n{result}", parse_mode="Markdown")
        user_states.pop(chat_id, None)
        return

    # === Категорії ===
    if state["stage"] == "category":
        if text == "Пироги":
            state["stage"] = "pies_sub"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("З мʼясом", "Без мʼяса", "Солодкі")
            markup.add("↩ Назад")
            bot.send_message(chat_id, "Оберіть підкатегорію пирогів:", reply_markup=markup)

        elif text == "Пиріжки":
            state["stage"] = "pyrizhky_sub"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("Солоні", "Солодкі")
            markup.add("↩ Назад")
            bot.send_message(chat_id, "Оберіть підкатегорію:", reply_markup=markup)

        elif text == "Галети":
            state["stage"] = "galety"
            send_product_buttons(chat_id, galety)

        elif text == "Десерти":
            state["stage"] = "deserty"
            send_product_buttons(chat_id, deserty)

    # === Підкатегорії пирогів ===
    elif state["stage"] == "pies_sub":
        if text == "↩ Назад":
            return start_report(message)
        if text in pies:
            state["stage"] = "pies_select"
            state["current_dict"] = pies[text]
            send_product_buttons(chat_id, pies[text])

    # === Підкатегорії пиріжків ===
    elif state["stage"] == "pyrizhky_sub":
        if text == "↩ Назад":
            return start_report(message)
        if text == "Солоні":
            state["stage"] = "savory_pyrizhky"
            state["current_dict"] = savory_pyrizhky
            send_product_buttons(chat_id, savory_pyrizhky)
        elif text == "Солодкі":
            state["stage"] = "sweet_pyrizhky"
            state["current_dict"] = sweet_pyrizhky
            send_product_buttons(chat_id, sweet_pyrizhky)

    # === Натискання на кнопку виробу ===
    elif "current_dict" in state and text in state["current_dict"]:
        state["waiting_for_count"] = text
        bot.send_message(chat_id, f"Скільки залишилось з {text}?")

    # === Введення кількості ===
    elif "waiting_for_count" in state:
        emoji = state["waiting_for_count"]
        name = state["current_dict"][emoji]
        user_reports[chat_id].append(f"{emoji} {name} — {text} шт.")
        state.pop("waiting_for_count")
        send_product_buttons(chat_id, state["current_dict"])

# === КНОПКИ З ТОВАРАМИ ===
def send_product_buttons(chat_id, data):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keys = list(data.keys())
    for i in range(0, len(keys), 2):
        row = keys[i:i + 2]
        markup.add(*row)
    markup.add("/готово")
    bot.send_message(chat_id, "Оберіть виріб:", reply_markup=markup)

# === СТАРТ БОТА ===
bot.infinity_polling()
