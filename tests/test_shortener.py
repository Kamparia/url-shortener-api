import os
import pytest
from dotenv import load_dotenv

from api.shortener import hash_url, validate_url, Shortener, ShortenerError
from api.shortener import UrlResponse


load_dotenv()  # load .env file


# test data
LONG_URL = "https://google.com"
HASH_VALUE = "05046f26"


@pytest.fixture
def shortener():
    return Shortener()


def test_hash_url():
    """
    Test that the hash_url function
    :return:
    """
    result = hash_url(LONG_URL)
    assert result == HASH_VALUE
    assert len(result) == 8
    assert type(result) == str


def test_validate_url():
    assert validate_url(LONG_URL) is True
    assert validate_url('google.com') is False


def test_shortener_shorten(shortener):
    data = shortener.shorten(LONG_URL)
    assert type(data) == UrlResponse
    assert data.long_url == LONG_URL
    assert data.short_url == f'{os.getenv("ROOT_DOMAIN")}/{HASH_VALUE}'
    assert data.clicks is not None


def test_shortener_shorten_invalid_url(shortener):
    with pytest.raises(ShortenerError):
        shortener.shorten('google.com')


def test_shortener_get_url(shortener):
    response = shortener.get_url(HASH_VALUE)
    assert response.long_url == LONG_URL
    assert response.short_url == f'{os.getenv("ROOT_DOMAIN")}/{HASH_VALUE}'
    assert response.clicks is not None


def test_shortener_get_url_invalid_hash(shortener):
    with pytest.raises(ShortenerError):
        shortener.get_url('invalid_hash')


def test_shortener_expand(shortener):
    long_url = shortener.expand(HASH_VALUE)
    assert long_url == LONG_URL


def test_shortener_expand_invalid_hash(shortener):
    with pytest.raises(ShortenerError):
        shortener.expand('invalid_hash')
