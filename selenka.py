from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pymysql.cursors
import unittest

# export PATH=$PATH:/Users/porczi/Downloads/chromedriver


class oto_moto_search(unittest.TestCase):

    def assert_quote(self, title):  # assertion on the first quote
        self.wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'offer-title__link')))
        quote_after_sort = self.driver.find_element_by_class_name(
            "offer-title__link")
        self.assertIn(title, quote_after_sort.text)

    def wait_until_clickable(self, ByFn, path):
        self.wait.until(EC.element_to_be_clickable(
            (ByFn, path)))

    def get_quote_details(self, quote):

        price_details = quote.find_element_by_class_name(
            "offer-item__price")
        price = price_details.find_element_by_xpath(
            ".//span[1]/span[1]").text
        price = price.replace(" ", "")

        title = quote.find_element_by_xpath(
            ".//div[@class='offer-item__title']/h2").text

        ID = quote.find_element_by_xpath(
            ".//div[@class='offer-item__title']/h2/a").get_attribute("data-ad-id")

        img_src = quote.find_element_by_xpath(
            ".//div[@class='offer-item__photo  ds-photo-container']/a/img").get_attribute("src")
        location = quote.find_element_by_xpath(
            ".//div[@class='offer-item__content ds-details-container']/h4/span[2]").text
        region = quote.find_element_by_xpath(
            ".//div[@class='offer-item__content ds-details-container']/h4/span[3]").text
        region = region.replace("(", "")
        region = region.replace(")", "")

        return {"title": title, "price": price, "ID": ID, "img_src": img_src, "location": location, "region": region}

    def setUp(self):
        self.driver = Chrome()
        self.wait = WebDriverWait(self.driver, 15)

    def test_search_in_oto_moto(self):
        driver = self.driver
        wait = self.wait

        driver.get("https://otomoto.pl")
        self.assertIn("OTOMOTO", driver.title)

        # entering brand of car \/\/\/

        brand = driver.find_element_by_id(
            "filter_enum_make")
        brand.send_keys("BMW")
        brand.send_keys(Keys.RETURN)

        # entering model of car \/\/\/

        self.wait_until_clickable(By.ID, "filter_enum_model")
        model = driver.find_element_by_id(
            "filter_enum_model")
        model.send_keys("seria 3")
        model.send_keys(Keys.RETURN)

        wait.until(EC.element_to_be_clickable(
            (By.ID, 'filter_enum_generation')))

        # clicking search button \/\/\/

        search_button = driver.find_element_by_xpath(
            "//button[@class='ds-button ds-width-full']")
        search_button.click()

        self.assert_quote("BMW Seria 3")

        wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "select2-selection__arrow")))

        # closing cookies to continue \/\/\/

        wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'cookiesBarClose')))
        cookies = driver.find_element_by_class_name("cookiesBarClose")
        cookies.click()

        # checking random quote's price \/\/\/

        price_before = driver.find_element_by_class_name(
            "offer-item__price")
        price_before_sort = price_before.find_element_by_xpath(
            ".//span[1]/span[1]").text
        price_before_sort = price_before_sort.replace(" ", "")

        # sorting by cheapest \/\/\/

        show_list = driver.find_element_by_id(
            "select2-order-select-gallery-container")
        show_list.click()
        wait.until(EC.element_to_be_clickable(
                   (By.XPATH, "//ul[@id='select2-order-select-gallery-results']/li[3]")))
        lowest_price = driver.find_element_by_xpath(
            "//ul[@id='select2-order-select-gallery-results']/li[3]")
        lowest_price.click()

        # waiting for the page to load \/\/\/

        pictures = driver.find_element_by_xpath(
            "//div[contains(@class, 'offer-item__photo  ds-photo-container')]/a")

        wait.until(EC.staleness_of(pictures))

        self.assert_quote("BMW Seria 3")

        # assertion of the first quote after sorting \/\/\/

        first_price_details = driver.find_element_by_class_name(
            "offer-item__price")
        price = first_price_details.find_element_by_xpath(
            ".//span[1]/span[1]").text
        price = price.replace(" ", "")

        second_price_details = driver.find_elements_by_xpath(
            "//div[contains(@class, 'offer-item__price')]")[1]

        # assertion of the second quote after sorting \/\/\/

        price_two = second_price_details.find_element_by_xpath(
            ".//span[1]/span[1]").text
        price_two = price_two.replace(" ", "")

        # checking if SORTED CORRECTLY \/\/\/

        self.assertLessEqual(int(price), int(price_before_sort))
        self.assertLessEqual(int(price), int(price_two))

        # all quotes on page \/\/\/
        quotes = driver.find_elements_by_xpath(
            "//div[@class='offers list']/article")

        quotes_details = []

        for i in range(0, 3):
            details = self.get_quote_details(quotes[i])
            quotes_details.append(details)

        # CONNECTING TO dockerMySql \/\/\/:

        connection = pymysql.connect(host='localhost',
                                     user='sara',
                                     password='sarka',
                                     db='OtoMoto',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                for i in quotes_details:
                    sql = "CREATE TABLE IF NOT EXISTS OtoMoto.bmw (title varchar(50) , PLN varchar(50), id varchar(50), location varchar(50), region varchar(50), img varchar(500))"
                    cursor.execute(sql)
                    # Create a new record
                    sql = "INSERT INTO OtoMoto.bmw (title, PLN, id, location, region, img) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(
                        sql, (i["title"], i["price"], i["ID"], i["location"], i["region"], i["img_src"]))
                    connection.commit()
        finally:
            connection.close()

    def tear_down(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
