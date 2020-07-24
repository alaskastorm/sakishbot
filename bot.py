from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters

from time import sleep

from parser import NikeParser


TG_TOKEN = ""


def message_handler(bot: Bot, update: Update):
    text = update.effective_message.text
    compare_var = ""

    if '/lit' in text:
        while True:
            output_message = NikeParser().run_and_send_to_bot()
            if output_message != compare_var:
                compare_var = output_message

                bot.send_message(chat_id=int, text=compare_var)

            sleep(600)


def main():
    bot = Bot(token=TG_TOKEN)
    updater = Updater(bot=bot)
    handler = MessageHandler(Filters.all, message_handler)
    updater.dispatcher.add_handler(handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()