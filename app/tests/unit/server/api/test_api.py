from app.app import create_app
import pytest
from app.server.db.models import AuthToken
from app.server.db.models import Url
from app.server.db.extensions import db

testing_app = create_app(config_file="../tests/settings.py")


@pytest.fixture(scope="session")
def authorization_header():
    """
    Provides a valid authorization HEADER for the application under test.
    """
    with testing_app.app_context():
        return {
            "Authorization": f"Bearer {AuthToken.query.filter_by(auth_token=testing_app.secret_key).first()}"
        }


@pytest.mark.parametrize(
    "url,expected_response",
    [("https://www.google.com", 200), ("https://www.fakeblock.com", 404)],
)
def test_post_shorten_response_code(authorization_header, url, expected_response):
    """
    Verifies the expected response code for a POST request to the /api/shorten endpoint.
    """
    response = testing_app.test_client().post(
        "/api/shorten", headers=authorization_header, data={"url": url}
    )
    assert (
        response.status_code == expected_response
    ), f"Expected a {expected_response} response for URL {url} but got {response.status_code}"


@pytest.mark.parametrize(
    "url,expected_response",
    [("https://www.google.com", True), ("https://www.fakeblock.com", False)],
)
def test_post_shorten_success_status(authorization_header, url, expected_response):
    """
    Verifies the expected "success" status for a POST request to the /api/shorten endpoint.
    """
    response = testing_app.test_client().post(
        "/api/shorten", headers=authorization_header, data={"url": url}
    )
    response_data = response.json
    assert (
        response_data["success"] == expected_response
    ), f"Expected 'success' to be {expected_response}, not {response_data['success']}"


def test_post_shorten_validate_url(authorization_header):
    """
    Verifies that the shortened URL returned by the /api/shorten endpoint matches the value stored in the database
    for that value.
    """
    url = "https://www.wikipedia.org"
    shortened_url = (
        testing_app.test_client()
        .post("/api/shorten", headers=authorization_header, data={"url": url})
        .json["short_url"]
    )
    with testing_app.app_context():
        assert (
            db.session.query(Url)
            .filter(Url.original_url == url, Url.short_url == shortened_url)
            .first()
        ), f"Expected to find a database record for a URL with original_url {url} and short_url {shortened_url}, but none exists"
