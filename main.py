import logging

import bs4
import requests


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('nike')


class NikePrice:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {'accept': '*/*',
                                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

    def load_page(self):
        url = "https://www.nike.com/ru/w/mens-air-max-270-shoes-1m67gz5ix6dznik1zy7ok"
        result = self.session.get(url)
        result.raise_for_status()
        return result.text

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select("div.product-card.css-1wapeca.css-z5nr6i.css-11ziap1.css-zk7jxt.css-dpr2cn.product-grid__card")

        for block in container:
            self.parse_block(block.select_one("div.product-price.css-11s12ax.is--current-price"))

    def parse_block(self, block):
        logger.info(block)
        # discount_price = container.select_one("div.product-price.is--current-price.css-s56yt7").text
        # if not discount_price:
        #     logger.error("No discount_price")
        #
        # full_price = container.select_one("div.product-price.css-31z3ik.css-ndethb.product-price-reduced").text
        # if not full_price:
        #     logger.error("No full_price")
        #
        # available_sizes = container.find("label").text
        # if not available_sizes:
        #     logger.error("No available_sizes")
        #
        # logger.info("Со скидкой: {}\nБез скидки: {}\nДоступные размеры: {}".format(
        #     discount_price, full_price, available_sizes))



    def run(self):
        text = self.load_page()
        self.parse_page(text)


if __name__ == "__main__":
    parser = NikePrice()
    parser.run()