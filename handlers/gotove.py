from .state import bot
from telebot import types

def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🥧 Готове", callback_data="готове"))
    bot.send_message(chat_id, "З чого почнемо?", reply_markup=markup)

def show_gotove_menu(call):
    chat_id = call.message.chat.id
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🥧 Пироги", callback_data="готове_pies"),
        types.InlineKeyboardButton("🥟 Пиріжки", callback_data="готове_pyrizhky"),
        types.InlineKeyboardButton("✅ Завершити", callback_data="завершити")
    )
    bot.send_message(chat_id, "Оберіть категорію:", reply_markup=markup)

def show_pies_list(call):
    chat_id = call.message.chat.id
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🍗🍅🧀", callback_data="пиріг_🍗🍅🧀"),
        types.InlineKeyboardButton("🍗🍍", callback_data="пиріг_🍗🍍"),
        types.InlineKeyboardButton("🔚 З пирогами — все", callback_data="готове")
    )
    bot.send_message(chat_id, "Оберіть пиріг:", reply_markup=markup)
