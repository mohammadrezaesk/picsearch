import pymongo

import config


class MongoClient:
    def __init__(self):
        self._client = pymongo.MongoClient(config.MONGO_HOST_URL)

        self._db = self._client[config.MONGO_DB]
        self._collection = self._db[config.MONGO_COLLECTION]
        self._collection.create_index([("id", 1)], unique=True)

    def remove_object_id(self, doc):
        if "_id" in doc:
            del doc["_id"]
        return doc

    def get_products_by_ids(self, products_ids):
        data = list(self._collection.find({"id": {"$in": products_ids}}))
        clean_result = [self.remove_object_id(doc) for doc in data]

        return clean_result
