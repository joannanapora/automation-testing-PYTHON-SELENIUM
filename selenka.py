from __future__ import unicode_literals
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import unittest

# export PATH=$PATH:/Users/porczi/Downloads/chromedriver


class oto_moto_search(unittest.TestCase):

    def assert_quote(self, title):
        self.wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'offer-title__link')))
        quote_after_sort = self.driver.find_element_by_class_name(
            "offer-title__link")
        self.assertIn(title, quote_after_sort.text)

    def wait_until_clickable(self, ByFn, path):
        self.wait.until(EC.element_to_be_clickable(
            (ByFn, path)))

    def setUp(self):
        self.driver = Chrome()
        self.wait = WebDriverWait(self.driver, 15)

    def test_search_in_oto_moto(self):
        driver = self.driver
        wait = self.wait

        driver.get("https://otomoto.pl")
        self.assertIn("OTOMOTO", driver.title)

        brand = driver.find_element_by_id("filter_enum_make")
        brand.send_keys("BMW")
        brand.send_keys(Keys.RETURN)

        self.wait_until_clickable(By.ID, "filter_enum_model")
        model = driver.find_element_by_id("filter_enum_model")
        model.send_keys("seria 3")
        model.send_keys(Keys.RETURN)

        wait.until(EC.element_to_be_clickable(
            (By.ID, 'filter_enum_generation')))

        search_button = driver.find_element_by_xpath(
            "//button[@class='ds-button ds-width-full']")
        search_button.click()

        self.assert_quote("BMW Seria 3")

        wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "select2-selection__arrow")))

        wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'cookiesBarClose')))
        cookies = driver.find_element_by_class_name("cookiesBarClose")
        cookies.click()

        price_before = driver.find_element_by_class_name("offer-item__price")
        price_before_sort = price_before.find_element_by_xpath(
            ".//span[1]/span[1]").text
        price_before_sort = price_before_sort.replace(" ", "")
        print("Price of first quote before sort:", price_before_sort)

        show_list = driver.find_element_by_id(
            "select2-order-select-gallery-container")
        show_list.click()

        wait.until(EC.element_to_be_clickable(
                   (By.XPATH, "//ul[@id='select2-order-select-gallery-results']/li[3]")))
        lowest_price = driver.find_element_by_xpath(
            "//ul[@id='select2-order-select-gallery-results']/li[3]")
        lowest_price.click()

        pictures = driver.find_element_by_xpath(
            "//body/div[@id='siteWrap']/div[@id='listContainer']/section[@id='body-container']/div[2]/div[1]/div[1]/div[1]/div[5]/article[1]/div[1]/a[1]/img[1]")

        wait.until(EC.staleness_of(pictures))

        self.assert_quote("BMW Seria 3")

        first_price_details = driver.find_element_by_class_name(
            "offer-item__price")
        price = first_price_details.find_element_by_xpath(
            ".//span[1]/span[1]").text
        price = price.replace(" ", "")
        print("Price of first quote: ", price)

        second_price_details = driver.find_elements_by_xpath(
            "//div[contains(@class, 'offer-item__price')]")[1]

        price2 = second_price_details.find_element_by_xpath(
            ".//span[1]/span[1]").text
        price2 = price2.replace(" ", "")
        print("Price of second quote: ", price2)

        # checking if sorts correctly
        self.assertLessEqual(int(price), int(price2))

    def tear_down(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
