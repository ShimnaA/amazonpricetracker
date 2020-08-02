from amazon_config import (
    get_chrome_web_driver,
    get_web_driver_options,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    DIRECTORY,
    NAME,
    CURRENCY,
    MIN_PRICE,
    MAX_PRICE,
    FILTERS,
    BASE_URL
)
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

class GenerateReport:
    def __init__(self):
        pass

class AmazonAPI:
    def __init__(self, search_term, filters, base_url, currency):
        self.search_term = search_term
        self.base_url = base_url
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
        self.currency = CURRENCY
        self.price_filter = f"&rh=p_36%3A{FILTERS['min']}00-{FILTERS['max']}00"

    def run(self):
        print("Starting Script")
        print(f"Looking for {self.search_term} products")
        links = self.get_products_links()
        time.sleep(3)
        print(f"Got {len(links)} number of links")
        print("Getting info of products")
        print(links)
        products = self.get_products_info(links)
        self.driver.quit()

    def get_products_info(self, links):
        asins = self.get_asins(links)
        products = []
        for asin in asins:
            product = self.get_single_product_info(asin)



    def get_single_product_info(self, asin):
        print(f"Product ID: {asin} - getting data...")
        product_short_url = self.shorten_url(asin)
        print(product_short_url)

    def get_asins(self, links):
        return [self.get_asin(link) for link in links]

    def get_asin(self, product_link):
        return product_link[product_link.find('/dp/') + 4:product_link.find('/ref')]

    def shorten_url(self, asin):
        return self.base_url + 'dp/' + asin

    def get_products_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element_by_id("twotabsearchtextbox")
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        time.sleep(2)
        result_list = self.driver.find_elements_by_class_name("a-section.aok-relative.s-image-fixed-height")
        print(len(result_list))
        links = []
        try:
            links = [res.find_element_by_xpath("..").get_attribute('href') for res in result_list]
            return links
        except Exception as e:
            print("Didnt get any product")
            print(e)
            return links



if __name__ == '__main__':
    amazon = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    print(amazon.price_filter)
    amazon.run()
