import re

import pytest

from app.app import app
from app.server.db.models import Url
from app.server.db.extensions import db


@pytest.fixture(scope="session")
def ten_k_urls():
    """
    Inserts 10K new URL records into the test database and deletes them after the test.
    """
    test_url = "https://www.10k-url-test.com"
    with app.app_context():
        for _ in range(10_000):
            db.session.add(Url(original_url=test_url))
        db.session.commit()
        yield
        # Cleanup after all tests run
        db.session.query(Url).filter(Url.original_url == test_url).delete(synchronize_session=False)
        db.session.commit()


def test_generate_short_url_properties():
    """
    Verifies that Url.generate_short_url() generates a URL suffix of length 5 containing only letters and numbers.
    """
    with app.app_context():
        test_url = Url(original_url="https://www.wikipedia.org")
    assert re.match(re.compile("^[a-zA-Z0-9]{5}$"), test_url.short_url), f"Expected short_url to contain only 5 total letters and digits, but got {test_url.short_url}"


@pytest.mark.parametrize("run", range(100))
def test_generate_short_url_unique(ten_k_urls, run):
    """
    Verifies that Url.generate_short_url() generates a unique URL
    """
    with app.app_context():
        test_url = Url(original_url="https://www.wikipedia.org")
        assert not Url.query.filter(Url.short_url == test_url.short_url).first(), "New URL objects must have a unique short URL"
