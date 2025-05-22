from .state import bot, user_states, user_reports
from telebot import types
from handlers.gotove import show_gotove_menu

@bot.message_handler(commands=['звіт'])
def start_report(message):
    chat_id = message.chat.id
    user_reports[chat_id] = {"локація": None, "готове": {}}
    user_states[chat_id] = "вибір_локації"

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📍 Руська, 3", callback_data="локація_руська"),
        types.InlineKeyboardButton("📍 Лепкого, 6", callback_data="локація_лепкого")
    )
    bot.send_message(chat_id, "Оберіть локацію для звіту:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("локація_"))
def handle_location(call):
    chat_id = call.message.chat.id
    location = "Руська, 3" if "руська" in call.data else "Лепкого, 6"
    user_reports[chat_id]["локація"] = location
    user_states[chat_id] = "main_menu"

    from handlers.gotove import show_main_menu
    show_main_menu(chat_id)
