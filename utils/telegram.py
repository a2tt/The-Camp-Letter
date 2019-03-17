import telegram

import settings

bot = telegram.Bot(settings.TELEGRAM_TOKEN)


def send_message(message, chat_id=settings.TELEGRAM_CHAT_ID):
    resp = bot.send_message(chat_id=chat_id, text=message, timeout=5)
