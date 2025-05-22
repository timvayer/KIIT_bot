from .state import bot, user_reports
from telebot import types

@bot.callback_query_handler(func=lambda call: call.data == "готове_pyrizhky")
def show_pyrizhky_menu(call):
    chat_id = call.message.chat.id

    # Заголовки
    bot.send_message(chat_id, "*Солоні пиріжки:*", parse_mode="Markdown")
    bot.send_message(chat_id, ".")
    bot.send_message(chat_id, "*Солодкі пиріжки:*", parse_mode="Markdown")
    bot.send_message(chat_id, " ")

    markup = types.InlineKeyboardMarkup(row_width=2)

    # Солоні
    markup.add(
        types.InlineKeyboardButton("🥔", callback_data="пиріжок_🥔"),
        types.InlineKeyboardButton("🥔🍄", callback_data="пиріжок_🥔🍄"),
        types.InlineKeyboardButton("🍄", callback_data="пиріжок_🍄"),
        types.InlineKeyboardButton("🥬", callback_data="пиріжок_🥬"),
        types.InlineKeyboardButton("🥬🥩", callback_data="пиріжок_🥬🥩"),
        types.InlineKeyboardButton("🥩🥗🐄", callback_data="пиріжок_🥩🥗🐄"),
        types.InlineKeyboardButton("🍗🍄", callback_data="пиріжок_🍗🍄")
    )

    # Солодкі
    markup.add(
        types.InlineKeyboardButton("🍒", callback_data="пиріжок_🍒"),
        types.InlineKeyboardButton("🍒🍫", callback_data="пиріжок_🍒🍫"),
        types.InlineKeyboardButton("🍒🌺", callback_data="пиріжок_🍒🌺"),
        types.InlineKeyboardButton("🍐", callback_data="пиріжок_🍐"),
        types.InlineKeyboardButton("Слива", callback_data="пиріжок_слива"),
        types.InlineKeyboardButton("Абрикос", callback_data="пиріжок_абрикос"),
        types.InlineKeyboardButton("🌺", callback_data="пиріжок_🌺"),
        types.InlineKeyboardButton("Мак крем", callback_data="пиріжок_мак")
    )

    markup.add(types.InlineKeyboardButton("🔚 З пиріжками — все", callback_data="готове"))
    bot.send_message(chat_id, "Оберіть пиріжки:", reply_markup=markup)
