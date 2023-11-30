import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from get_tempo import get_today, get_tomorrow

# Set up logging for troubleshooting
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Set up keyboard
reply_keyboard = [
    ["/today"],
    ["/tomorrow"],
]
markup = ReplyKeyboardMarkup(reply_keyboard)

# Logic in response to /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi there! This bot tells you whether today is a BLUE, WHITE or RED day, according to EDF's Tempo Contract.", reply_markup=markup)


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Logic to get today's label
    tdy = get_today()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Today is a {tdy} day.", reply_markup=markup)


async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Logic to get today's label
    tmr = get_tomorrow()
    if tmr:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Tomorrow is a {tmr} day.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"The Tempo colour for tomorrow is not defined yet.", reply_markup=markup)


if __name__ == '__main__':
    # Create application object
    with open("creds.json") as f:
        token = eval(f.read())["TelegramToken"]
    application = ApplicationBuilder().token(token).build()
    
    # start command handler
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    today_handler = CommandHandler('today', today)
    application.add_handler(today_handler)

    tomorrow_handler = CommandHandler('tomorrow', tomorrow)
    application.add_handler(tomorrow_handler)
    
    application.run_polling()