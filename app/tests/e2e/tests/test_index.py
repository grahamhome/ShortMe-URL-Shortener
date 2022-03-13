import os
import re

from selenium import webdriver
import pytest

from app.server.db.models import Url
from app.tests.e2e.page_objects.index import Index
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(os.environ["SQLALCHEMY_DATABASE_URI"])
session = Session(bind=engine)

shortened_url_pattern = re.compile("^" + os.environ["HOST"] + "/([a-zA-Z0-9]{5})$")


@pytest.fixture(scope="session")
def driver():
    """
    Provides a Chrome instance for the test session.
    """
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def index_page(driver):
    """
    Loads the index page of the application under test in the Chrome browser.
    """
    index_page = Index(driver)
    index_page.go()
    return index_page


@pytest.mark.parametrize("url", ["https://www.google.com"])
def test_shorten_valid_url_properties(index_page, url):
    """
    Verify that the shortened URL produced by inputting a valid URL to the index page
    has a suffix of length 5 consisting of numbers and letters.
    """
    shortened_url = index_page.shorten_url(url).get_shortened_url()
    assert re.match(
        shortened_url_pattern, shortened_url
    )


def test_shorten_valid_url_match(index_page):
    """
    Verify that the shortened URL produced by inputting a valid URL to the index page
    matches the value stored in the database for that value.
    """
    url = "https://www.wikipedia.org"
    shortened_url = index_page.shorten_url(url).get_shortened_url()
    assert (
        session.query(Url)
        .filter(
            Url.original_url == url,
            Url.short_url
            == re.match(
                shortened_url_pattern,
                shortened_url,
            ).group(1),
        )
        .first()
    ), f"Expected to find a database record for a URL with original_url {url} and short_url {shortened_url}, but none exists"
