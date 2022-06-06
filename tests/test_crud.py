import pytest
from pymongo import MongoClient

from api.crud import Database, mongo_connect


# test data
LONG_URL = "https://google.com"
HASH_VALUE = "05046f26"


def test_mongo_connect():
    """
    Test the connection to the mongo database
    """
    client = mongo_connect()
    assert client is not None
    assert type(client) is MongoClient


@pytest.fixture()
def mongo():
    """
    Create a mock mongo client
    """
    # set up
    db = Database(mongo_connect())
    db.add_url(LONG_URL, HASH_VALUE)
    yield db
    # tear down
    db.delete_url(HASH_VALUE)


def test_database_add_url(mongo):
    """
    Test the add_url function
    """
    mongo.add_url(LONG_URL, HASH_VALUE)
    assert mongo.url_exists(HASH_VALUE) is True


def test_database_get_url(mongo):
    """
    Test the get_url function
    """
    data = mongo.get_url(HASH_VALUE)
    assert data["long_url"] == LONG_URL
    assert data["hash_value"] == HASH_VALUE
    assert data["clicks"] is not None


def test_database_get_url_not_found(mongo):
    """
    Test the get_url function with a hash value that does not exist
    """
    data = mongo.get_url("12345")
    assert data is None


def test_database_url_exists(mongo):
    """
    Test the url_exists function
    """
    assert mongo.url_exists(HASH_VALUE) is True
    assert mongo.url_exists("12345") is False


def test_database_get_all_urls(mongo):
    """
    Test the get_all_urls function
    """
    data = mongo.get_all_urls()
    assert type(data) is list


def test_database_update_url_clicks(mongo):
    """
    Test the update_url_clicks function
    """
    old_data = mongo.get_url(HASH_VALUE)
    mongo.update_url_clicks(HASH_VALUE)
    new_data = mongo.get_url(HASH_VALUE)
    assert old_data["clicks"] + 1 == new_data["clicks"]


def test_database_delete_url(mongo):
    """
    Test the delete_url function
    """
    pass


def test_database_delete_url_not_found(mongo):
    """
    Test the delete_url function with a hash value that does not exist
    """
    assert mongo.delete_url("12345") is None
