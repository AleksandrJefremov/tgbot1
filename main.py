import os
import telebot
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = str(os.environ.get('BOT_TOKEN'))

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    print("Sending custom msg")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    print("sending msg")


bot.infinity_polling()
