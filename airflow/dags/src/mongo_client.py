import logging

import pymongo
from pymongo.errors import BulkWriteError

logger = logging.getLogger(__name__)


class MongoClient:
    BATCH_SIZE = 500

    def __init__(self, mongo_host_url, mongo_db, mongo_collection):
        self._client = pymongo.MongoClient(mongo_host_url)
        self._db = self._client[mongo_db]
        self._collection = self._db[mongo_collection]

    def insert_documents(self, products):
        for i in range(0, len(products), MongoClient.BATCH_SIZE):
            try:
                self._collection.insert_many(
                    documents=products[i : i + MongoClient.BATCH_SIZE], ordered=False
                )
                logger.info("Added {} documents".format(MongoClient.BATCH_SIZE))
            except BulkWriteError as e:
                for error in e.details["writeErrors"]:
                    if "duplicate key error" not in error["errmsg"]:
                        raise e
