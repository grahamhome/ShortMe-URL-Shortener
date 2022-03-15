import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC


class Page:
    load_time = 20
    url = None

    def __init__(self, driver):
        self.driver = driver

    def go(self):
        self.driver.get(f"{os.environ.get('HOST')}{self.url}")

    def get_element(self, element):
        """
        Given a tuple of (By, string), waits for the given element to be visible and returns its Selenium representation.
        """
        try:
            WebDriverWait(self.driver, self.load_time).until(
                EC.visibility_of_element_located(element)
            )
            return self.driver.find_element(*element)
        except TimeoutException:
            raise RuntimeError(
                f"Web element {element} did not load on page {self.url} after {self.load_time} seconds"
            )
