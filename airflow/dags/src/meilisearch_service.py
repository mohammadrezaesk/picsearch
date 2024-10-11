import meilisearch


class MeiliSearchService:
    def __init__(self):
        self.client = meilisearch.Client("http://meilisearch:7700", "testing_key")
        self.client.create_index(uid="products", options={"primaryKey": "id"})
        self.products_index = self.client.index("products")

    def get_products(self, query: str, count: int):
        return self.products_index.search(query, {"limit": count})

    def upsert_products(self, products: dict):
        self.products_index.add_documents(products)
