import re

import pytest
from app.server.db.models import Url
from app.server.db.extensions import db
from app.app import create_app
from string import digits, ascii_letters


testing_app = create_app(config_file="../tests/settings.py")


@pytest.fixture
def url():
    """
    Provides a URL instance for testing purposes.
    """
    with testing_app.app_context():
        return Url(original_url="https://www.google.com")


@pytest.fixture(scope="session")
def ten_thous_urls():
    """
    Inserts 10K URL records into the DB for testing and deletes them after the test.
    """
    url = "https://www.10ktesturl.com"
    with testing_app.app_context():
        for _ in range(10_000):
            test_url = Url(original_url=url)
            db.session.add(test_url)
        db.session.commit()
        yield
        db.session.query(Url).filter(Url.original_url == url).delete(
            synchronize_session=False
        )
        db.session.commit()


def test_short_url_properties(url):
    """
    Verifies that Url.generate_short_url() generates a URL suffix of length 5 and containing only numbers and letters.
    """
    with testing_app.app_context():
        short_url = url.generate_short_url()
    assert re.match(
        re.compile("^[a-zA-Z0-9]{5}$"), short_url
    ), f"Expected short URL to contain 5 total digits and letters, but got '{short_url}'"


def test_short_url_content(url):
    """
    Verifies that Url.generate_short_url() generates a URL suffix .
    """
    with testing_app.app_context():
        short_url = url.generate_short_url()
    assert set(short_url).issubset(
        digits + ascii_letters
    ), f"Expected short URL to contain ASCII letters and numbers only."


@pytest.mark.parametrize("run", range(100))
def test_short_url_no_duplicates(ten_thous_urls, run):
    """
    Verifies that Url.generate_short_url() does not produce duplicate URL suffixes.
    """
    url = Url(original_url="https://www.google.com")
    assert not Url.query.filter_by(
        short_url=url.short_url
    ).first(), "New Url objects must have unique short Url attribute."
