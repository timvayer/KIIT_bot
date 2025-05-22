from .state import bot, user_states, user_reports
from telebot import types

def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🥧 Готове", callback_data="готове"),
        types.InlineKeyboardButton("🥶 Заморозка", callback_data="заморозка"),
        types.InlineKeyboardButton("🥛 Молоко", callback_data="молоко"),
        types.InlineKeyboardButton("💧 Напої", callback_data="напої"),
        types.InlineKeyboardButton("🧃 Соки", callback_data="соки"),
        types.InlineKeyboardButton("☕️ Кава / Матча / Чаї", callback_data="кава"),
        types.InlineKeyboardButton("📦 Розхідники", callback_data="розхідники"),
        types.InlineKeyboardButton("✅ Завершити звіт", callback_data="завершити")
    )
    bot.send_message(chat_id, "З чого почнемо?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "готове")
def show_gotove_menu(call):
    chat_id = call.message.chat.id
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🥧 Пироги", callback_data="готове_pies"),
        types.InlineKeyboardButton("🥟 Пиріжки", callback_data="готове_pyrizhky"),
        types.InlineKeyboardButton("🥧 Галети", callback_data="готове_galety")
    )
    bot.send_message(chat_id, "Що звітуємо першим?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "готове_pies")
def show_pies_list(call):
    chat_id = call.message.chat.id

    # Надсилаємо секції
    bot.send_message(chat_id, "*Мʼясні пироги:*", parse_mode='Markdown')
    bot.send_message(chat_id, ".")
    bot.send_message(chat_id, "*Немʼясні пироги:*", parse_mode='Markdown')
    bot.send_message(chat_id, ".")
    bot.send_message(chat_id, "*Солодкі пироги:*", parse_mode='Markdown')
    bot.send_message(chat_id, " ")

    # Формуємо кнопки
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🍗🍅🧀", callback_data="пиріг_🍗🍅🧀"),
        types.InlineKeyboardButton("🍗🍍", callback_data="пиріг_🍗🍍"),
        types.InlineKeyboardButton("🍗🍄🧀", callback_data="пиріг_🍗🍄🧀"),
        types.InlineKeyboardButton("🐄🧀", callback_data="пиріг_🐄🧀"),
        types.InlineKeyboardButton("🦃🫑", callback_data="пиріг_🦃🫑"),
        types.InlineKeyboardButton("🧅", callback_data="пиріг_🧅"),
        types.InlineKeyboardButton("🍄🧀", callback_data="пиріг_🍄🧀"),
        types.InlineKeyboardButton("🧀🍃", callback_data="пиріг_🧀🍃"),
        types.InlineKeyboardButton("🧀", callback_data="пиріг_🧀"),
        types.InlineKeyboardButton("🍒🫐", callback_data="пиріг_🍒🫐"),
        types.InlineKeyboardButton("🍒🧀", callback_data="пиріг_🍒🧀")
    )
    markup.add(types.InlineKeyboardButton("🔚 З пирогами — все", callback_data="готове"))

    bot.send_message(chat_id, "Оберіть пиріг:", reply_markup=markup)
