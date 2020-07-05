import os
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                        ConversationHandler)
from models import create_connection, select_all_tasks
import datetime
from tzlocal import get_localzone
import pytz
import time
import logging
import csv

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
logger = logging.getLogger(__name__)
TOKEN = 'TELEGRAMBOTTOKEN'
conn = create_connection()
data = select_all_tasks(conn)
# births = [['21/09', 'Soldev'], ['06/05', 'Dummy'], ['10/04', 'Duny']]

def start(update, context):
    """Send a message when the command /start is issued."""
    chat_id = update.message.chat_id
    update.message.reply_text(
    """ 
    Hello guys!!
    Aku doscom birthday reminder, aku bakal ngingetin ulang tahun setiap anggota doscom ^_-
    """)
    jakarta = pytz.timezone('Asia/Jakarta')
    waktu = datetime.time(7,5, tzinfo=jakarta)
    print(waktu)
    job = context.job_queue.run_daily(cek_birth, time=waktu, context=chat_id, name=None)


def cek_birth(context):
    job = context.job
    logger.info('calling cek_birth')
    today = taim.strftime('%m-%d')
    berulang = [x[1] for x in data if today in x]
    if berulang:
        line = r'Wah... Hari ini ada yang ulang tahun nih Selamat ulang tahun ya '
        line += ', '.join(berulang)
    else:
        line = 'Belum ada yang berulang'     
            
    context.bot.send_message(job.context, text=line)
    berulang.clear()

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("""Halo, kalian bisa bantu bot ini biar lebih pinter
    di github.com/solehudindt/doscom-birth-reminder
    """)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    # updater.start_webhook(listen="0.0.0.0",
    #                         port=int(PORT),
    #                         url_path=TOKEN)
    # updater.bot.setWebhook('https://herokuname.herokuapp.com/' + TOKEN)
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
	main() 