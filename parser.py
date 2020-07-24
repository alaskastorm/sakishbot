import logging

import bs4
import requests


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('nike')


class NikeParser:

    def __init__(self):
        self.combined_data = ''
        self.counter = 1

        self.session = requests.Session()
        self.session.headers = {'accept': '*/*',
                                "user-agent":
                                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
                                    " like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

    def load_page(self):
        url = "https://www.nike.com/ru/w/mens-air-max-270-shoes-1m67gz5ix6dzapms5znik1zy7ok"

        try:
            result = self.session.get(url)
            result.raise_for_status()
            return result.text
        except Exception as e:
            logger.error(e)
            return "Connection Error: {}".format(e)

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')

        container = soup.select(
            "div.product-card.css-13vvinl.css-z5nr6i.css-11ziap1.css-zk7jxt.css-dpr2cn.product-grid__card")
        if not container:
            self.combined_data = "No container"
            logger.error(self.combined_data)
            return self.combined_data

        for block in container:
            self.parse_block(block)

    def parse_block(self, block):
        url_sneaker = block.select_one("a.product-card__link-overlay").get('href')
        if not url_sneaker:
            self.combined_data = "No url_sneaker"
            logger.error(self.combined_data)
            return self.combined_data

        name_sneaker = block.select_one("div.product-card__titles")
        if not name_sneaker:
            self.combined_data = "No name_sneaker"
            logger.error(self.combined_data)
            return self.combined_data

        full_price = block.select_one("div.product-price.css-31z3ik.css-ndethb.product-price-reduced")
        if not full_price:
            discount_price = "No discount price"
            full_price = block.select_one("div.product-price.css-11s12ax.is--current-price")
            if not full_price:
                self.combined_data = "No full_price"
                logger.error(self.combined_data)
                return self.combined_data
        else:
            discount_price = block.select_one("div.product-price.is--current-price.css-s56yt7")
            if not discount_price:
                self.combined_data = "No discount_price"
                logger.error(self.combined_data)
                return self.combined_data

        try:
            self.combined_data += "{}) {}\n\tFull price: {}\n\tDiscount price: {}\n\t{}\n\n".format(
                self.counter, name_sneaker.text, full_price.text, discount_price.text, url_sneaker)
        except (AttributeError, TypeError):
            self.combined_data += "{}) {}\n\tFull price: {}\n\tDiscount price: {}\n\t{}\n\n".format(
                self.counter, name_sneaker.text, full_price.text, discount_price, url_sneaker)

        logger.info(self.combined_data)

        self.counter += 1

    def run_and_send_to_bot(self):
        text = self.load_page()
        if "Connection Error:" in text:
            return text
        else:
            self.parse_page(text)
            return self.combined_data


# if __name__ == "__main__":
#     NikeParser().run_and_send_to_bot()