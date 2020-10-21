from __future__ import unicode_literals
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import unittest

# export PATH=$PATH:/Users/porczi/Downloads/chromedriver


class oto_moto_search(unittest.TestCase):
    def setUp(self):
        self.driver = Chrome()

    def test_search_in_oto_moto(self):
        driver = self.driver
        driver.get("https://otomoto.pl")
        self.assertIn("OTOMOTO", driver.title)

        brand = driver.find_element_by_id("filter_enum_make")
        brand.send_keys("BMW")
        brand.send_keys(Keys.RETURN)

        wait = WebDriverWait(driver, 10)
        model = wait.until(EC.element_to_be_clickable(
            (By.ID, 'filter_enum_model')))
        model.send_keys("seria 3")
        model.send_keys(Keys.RETURN)

        wait.until(EC.element_to_be_clickable(
            (By.ID, 'filter_enum_generation')))

        search_button = driver.find_element_by_xpath(
            "//button[@class='ds-button ds-width-full']")
        search_button.click()

        wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'offer-title__link')))

        quote1 = driver.find_element_by_class_name("offer-title__link")
        self.assertIn("BMW Seria 3", quote1.text)

        wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "select2-selection__arrow")))

        wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'cookiesBarClose')))
        cookies = driver.find_element_by_class_name("cookiesBarClose")
        cookies.click()

        show_list = driver.find_element_by_xpath(
            "//body/div[@id='siteWrap']/div[@id='listContainer']/div[@id='tabs-container']/div[1]/div[1]/form[1]/span[1]/span[1]/span[1]")
        show_list.click()

        wait.until(EC.element_to_be_clickable(
                   (By.XPATH, "//ul[@id='select2-order-select-gallery-results']/li[3]")))
        lowest_price = driver.find_element_by_xpath(
            "//ul[@id='select2-order-select-gallery-results']/li[3]")
        lowest_price.click()

        wait.until(EC.visibility_of_element_located((By.ID, "siteWrap")))

        wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'offer-title__link')))
        quote_after_sort = driver.find_element_by_class_name(
            "offer-title__link")
        self.assertIn("BMW Seria 3", quote_after_sort.text)

    def tear_down(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
