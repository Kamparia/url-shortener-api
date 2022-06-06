import os
import hashlib
import validators
from dotenv import load_dotenv

from api.crud import Database, mongo_connect
from api.schema import UrlResponse


load_dotenv()  # Load .env file


def hash_url(url: str) -> str:
    """
    Hash the url to a unique string.
    :param url: The url to hash.
    :return: The hash value.
    """
    return hashlib.sha256(url.encode('utf-8')).hexdigest()[:8]


def validate_url(url: str) -> bool:
    """
    Validate the url.
    :param url: The url to validate.
    :return: True if valid, False otherwise.
    """
    return bool(validators.url(url))


class Shortener:
    def __init__(self):
        client = mongo_connect()
        self.db = Database(client)
        self.root_url = os.getenv('ROOT_DOMAIN')

    def get_url(self, hash_value: str):
        """
        Get the url from the database.
        :param hash_value: The hash value of the url.
        :return: Return UrlResponse if the url is in the database.
        """
        short_url = f'{self.root_url}/{hash_value}'
        if self.db.url_exists(hash_value):
            url = self.db.get_url(hash_value)
            return UrlResponse(
                long_url=url['long_url'],
                short_url=short_url,
                clicks=url['clicks']
            )

        raise ShortenerError(f'Short Url ({short_url}) not found.')

    def shorten(self, long_url: str):
        """
        Shorten the long url to a unique string.
        :param long_url: The long url to shorten.
        :return: short_url: The shortened url
        """
        hash_value = hash_url(long_url)

        # check if url is valid
        if not validate_url(long_url):
            raise ShortenerError('Invalid URL. URL must start with http:// or https://')

        try:
            return self.get_url(hash_value)
        except ShortenerError:
            self.db.add_url(long_url=long_url, hash_value=hash_value)
            return UrlResponse(
                long_url=long_url,
                short_url=f'{self.root_url}/{hash_value}',
                clicks=0
            )

    def expand(self, hash_value: str):
        """
        Expand the short url to the long url.
        :param hash_value: The hash value of the short url.
        :return: long_url: The long url.
        """
        if not self.db.url_exists(hash_value):
            raise ShortenerError(f'Short Url ({hash_value}) not found.')

        self.db.update_url_clicks(hash_value)  # Update the clicks count
        return url['long_url'] if (url := self.db.get_url(hash_value)) else None


class ShortenerError(Exception):
    pass
