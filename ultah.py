from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                        ConversationHandler)
# from datetime import date, datetime
import time
import logging
import csv

with open('pengurus.csv', newline='') as f:
		reader = csv.reader(f)
		data = list(reader)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
logger = logging.getLogger(__name__)

births = [['21/09', 'Soldev'], ['06/05', 'Dummy'], ['10/04', 'Duny']]


def start(update, context):
    """Send a message when the command /start is issued."""
    chat_id = update.message.chat_id
    update.message.reply_text('Hello guys!! \nAku doscom birthday reminder, aku bakal ngingetin ulang tahun setiap anggota doscom ^_-')

    job = context.job_queue.run_daily(cek_birth, time=ttime(18,53), context=chat_id, name=None)


def cek_birth(context):
	job = context.job
	for x in births:
		today = time.strftime('%d/%m')
		line = 'Belum ada yang ulang tahun hari ini'

		if today in x[0]:
			line = 'Selamat ulang tahun ^_^ ' + x[1]
			break
	
	context.bot.send_message(job.context, text=line)

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("""Halo, kalian bisa bantu bot ini biar lebih pinter
    	di github.com/doscom-birth-reminder
    """)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
	main() 