import json

import meilisearch

import config


class MeiliSearchClient:
    def __init__(self):
        self.client = meilisearch.Client(config.MEILI_HOST_URL, config.MEILI_MASTER_KEY)
        self.client.create_index(uid="products", options={"primaryKey": "id"})
        self.products_index = self.client.index("products")

    def get_products(self, query: str, count: int):
        return self.products_index.search(query, {"limit": count})

    def upsert_products(self, products: dict):
        self.products_index.add_documents_json(json.dumps(products))
