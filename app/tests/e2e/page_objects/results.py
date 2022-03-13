from selenium.webdriver.common.by import By

from app.tests.e2e.page_objects.page import Page


class Results(Page):
    """
    Represents the elements and actions of the results page.
    """

    url = "/your_short_url"

    # Page elements
    # Output field
    _shortened_url_output = (By.XPATH, "//input[@id='copy-able']")

    def get_shortened_url(self):
        """
        Returns the shortened URL from the results page.
        """
        return self.get_element(self._shortened_url_output).get_attribute("value")
