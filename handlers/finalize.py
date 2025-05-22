from .state import bot, user_reports
from datetime import datetime, timedelta

@bot.callback_query_handler(func=lambda call: call.data == "завершити")
def complete_report(call):
    chat_id = call.message.chat.id
    now = datetime.utcnow() + timedelta(hours=3)
    weekday = {
        'Monday': 'понеділок', 'Tuesday': 'вівторок', 'Wednesday': 'середа',
        'Thursday': 'четвер', 'Friday': 'пʼятниця', 'Saturday': 'субота', 'Sunday': 'неділя'
    }[now.strftime('%A')]
    дата = now.strftime(f"🗓️ %d.%m.%Y, {weekday}")
    локація = user_reports.get(chat_id, {}).get("локація", "Локація не вказана")
    bot.send_message(chat_id, f"{дата}\n📍 {локація}\n\n(Звіт ще не заповнено.)")
