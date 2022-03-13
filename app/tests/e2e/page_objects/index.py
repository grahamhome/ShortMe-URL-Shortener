from selenium.webdriver.common.by import By

from app.tests.e2e.page_objects.page import Page
from app.tests.e2e.page_objects.results import Results


class Index(Page):
    """
    Represents the elements and actions of the index page.
    """

    url = "/"

    # Page elements
    # URL input field
    _url_input = (By.XPATH, "//input[@id='url-input']")
    _shorten_url_button = (By.XPATH, "//button[@type='submit']")

    def shorten_url(self, url):
        """
        Enters the given URL in the URL input field and clicks the "Shorten" button.
        """
        self.get_element(self._url_input).send_keys(url)
        self.get_element(self._shorten_url_button).click()
        return Results(self.driver)
