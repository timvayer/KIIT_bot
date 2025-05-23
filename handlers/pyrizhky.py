from .state import bot
from telebot import types

def show_pyrizhky_menu(call):
    chat_id = call.message.chat.id
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🥔", callback_data="пиріжок_🥔"),
        types.InlineKeyboardButton("🥔🍄", callback_data="пиріжок_🥔🍄"),
        types.InlineKeyboardButton("🔚 З пиріжками — все", callback_data="готове")
    )
    bot.send_message(chat_id, "Оберіть пиріжки:", reply_markup=markup)
