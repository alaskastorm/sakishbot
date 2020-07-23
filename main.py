from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters

import logging

import bs4
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('nike')

TG_TOKEN = ""


def message_handler(bot: Bot, update: Update):
    text = update.effective_message.text

    if '/lit' in text:
        output_message = NikeParse().run()
        bot.send_message(chat_id=update.effective_message.chat_id,
                         text=output_message)


class NikeParse:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {'accept': '*/*',
                                "user-agent":
                                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
                                    " like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

    def load_page(self):
        url = "https://www.nike.com/ru/w/mens-air-max-270-shoes-1m67gz5ix6dzapms5znik1zy7ok"
        result = self.session.get(url)
        # TODO: add "try except"
        result.raise_for_status()
        return result.text

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        # TODO: add "try except"
        container = soup.select(
            "div.product-card.css-13vvinl.css-z5nr6i.css-11ziap1.css-zk7jxt.css-dpr2cn.product-grid__card ")

        for block in container:
            self.parse_block(block)

    def parse_block(self, block):
        url_sneaker = block.select_one("a.product-card__link-overlay").get('href')
        if not url_sneaker:
            logger.error("No url_sneaker")
         # TODO: add "return" and recognize why
        name_sneaker = block.select_one("div.product-card__titles")
        if not name_sneaker:
            logger.error("No name_sneaker")

        full_price = block.select_one("div.product-price.css-31z3ik.css-ndethb.product-price-reduced")
        if not full_price:
            discount_price = "No discount price"
            full_price = block.select_one("div.product-price.css-11s12ax.is--current-price")
            if not full_price:
                logger.error("No full_price")
        else:
            discount_price = block.select_one("div.product-price.is--current-price.css-s56yt7")
            if not discount_price:
                logger.error("No discount_price")

        global combined_prices

        try:
            combined_prices += "{}\n\tFull price: {}\n\tDiscount price: {}\n{}\n\n".format(
                name_sneaker.text, full_price.text, discount_price.text, url_sneaker)
        except (AttributeError, TypeError):
            combined_prices += "{}\n\tFull price: {}\n\tDiscount price: {}\n{}\n\n".format(
                name_sneaker.text, full_price.text, discount_price, url_sneaker)

        logger.info(combined_prices)

    def run(self):
        text = self.load_page()
        self.parse_page(text)
        return combined_prices


def main():
    bot = Bot(token=TG_TOKEN)
    updater = Updater(bot=bot)
    handler = MessageHandler(Filters.all, message_handler)
    updater.dispatcher.add_handler(handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    combined_prices = ''
    main()