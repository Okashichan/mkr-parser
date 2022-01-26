import pymongo
from pymongo import MongoClient
from config import DATABASE_CONNECTION_STRING

cluster = MongoClient(DATABASE_CONNECTION_STRING)
db = cluster['telegram_db']
collection = db['telegram_db']


def test():
    print(cluster.list_database_names())


if __name__ == '__main__':
    test()