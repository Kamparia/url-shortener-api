import os
import pytest
from dotenv import load_dotenv

from api.schema import Url, Status, UrlResponse, Response


load_dotenv()  # Load .env file

# test data
LONG_URL = "https://google.com"
HASH_VALUE = "05046f26"
ROOT_DOMAIN = os.getenv('ROOT_DOMAIN')


def test_url():
    url = Url(
        long_url = LONG_URL,
        hash_value = '05046f26',
        clicks = 2
    )

    assert url.long_url == LONG_URL
    assert url.hash_value == HASH_VALUE
    assert url.clicks == 2
    assert url.created_at is not None
    assert url.deleted is False


def test_url_invalid_data():
    with pytest.raises(ValueError):
        Url(long_url=None, hash_value=HASH_VALUE, clicks=2)

    with pytest.raises(ValueError):
        Url(long_url=LONG_URL, hash_value=None, clicks=2)


def test_response():
    response = Response(
        status = Status.OK,
        code = 200,
        message = 'OK',
        data = None
    )

    assert response.status == Status.OK
    assert response.code == 200
    assert response.message == 'OK'
    assert response.data is None


def test_status_ok():
    status = Status.OK
    assert status == 'OK'


def test_status_error():
    status = Status.ERROR
    assert status == 'ERROR'


def test_url_response():
    url_response = UrlResponse(
        long_url = LONG_URL,
        short_url = f'{ROOT_DOMAIN}/{HASH_VALUE}',
        clicks=2
    )

    assert url_response.long_url == LONG_URL
    assert url_response.short_url == f'{ROOT_DOMAIN}/{HASH_VALUE}'
    assert url_response.clicks == 2
