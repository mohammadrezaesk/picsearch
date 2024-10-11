import os

# PINECONE
PINECONE_HOST_URL = os.getenv(
    "PINECONE_HOST_URL", "https://image-index-f6thjqr.svc.aped-4627-b74a.pinecone.io"
)
PINECONE_IMAGE_INDEX_NAME = os.getenv("PINECONE_IMAGE_INDEX_NAME", "image-index")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# GPT
GPT_API_KEY = os.getenv("GPT_API_KEY")
GPT_BASE_URL = os.getenv(
    "GPT_BASE_URL", "https://aiproxy.divar.dev/providers/openai/v1/"
)

# MONGO
MONGO_HOST_URL = os.getenv("MONGO_HOST_URL", "mongodb://mongo:27017")
MONGO_DB = os.getenv("MONGO_DB", "picsearch")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "products")

# MEILI
MEILI_HOST_URL = os.getenv("MEILI_HOST_URL", "http://meilisearch:7700")
MEILI_MASTER_KEY = os.getenv("MEILI_MASTER_KEY", "testing_key")
