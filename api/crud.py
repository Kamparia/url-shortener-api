import os
from dotenv import load_dotenv
from pymongo import MongoClient

from api.schema import Url


load_dotenv()  # load .env file


def mongo_connect() -> MongoClient:
    """ Connect to MongoDB instance """
    return MongoClient(os.getenv('MONGO_URI'))


class Database:
    """ Class for CRUD operation on MongoDB database """

    def __init__(self, client: MongoClient):
        """ Initialize database """
        self.db = client.get_database(os.getenv('MONGO_DB'))

    def add_url(self, long_url: str, hash_value: str) -> None:
        """ Add url to database """
        if not self.url_exists(hash_value):
            url = Url(long_url=long_url, hash_value=hash_value)
            self.db.urls.insert_one(url.__dict__)

    def get_url(self, hash_value: str) -> dict | None:
        """ Get url from database
        :param hash_value: hash value of url
        :return: Url object from database or None if not found
        """
        if self.url_exists(hash_value):
            return self.db.urls.find_one({'hash_value': hash_value})

        return None

    def get_all_urls(self) -> list:
        """ Get all urls from database """
        return list(self.db.urls.find())

    def url_exists(self, hash_value: str) -> bool:
        """ Check if url exists in database """
        return self.db.urls.find_one({'hash_value': hash_value}) is not None

    def update_url_clicks(self, hash_value: str) -> None:
        """ Update url clicks in database """
        if self.url_exists(hash_value):
            self.db.urls.update_one({'hash_value': hash_value},
                                    {'$inc': {'clicks': 1}})

    def delete_url(self, hash_value: str) -> None:
        """ Delete url from database """
        if self.url_exists(hash_value):
            self.db.urls.delete_one({'hash_value': hash_value})
