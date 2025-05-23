from .state import bot

def complete_report(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "Звіт завершено. Дякуємо!")
