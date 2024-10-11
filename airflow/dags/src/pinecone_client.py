import logging

from pinecone import Pinecone

logger = logging.getLogger(__name__)


class PineconeClient:
    def __init__(self, api_key: str, host_url: str, index_name: str):
        pc = Pinecone(api_key=api_key)
        self.index = pc.Index(name=index_name, host=host_url)
        logger.info("Pinecone connected ✅")
        logger.info(api_key)
        logger.info(host_url)

    def upsert_image(self, image_embeddings, image_ids):
        if len(image_embeddings) != len(image_ids):
            raise ValueError("Image embeddings must have same length")
        for i in range(0, len(image_embeddings), 128):
            vectors_to_upsert = [
                (image_id, embedding)
                for image_id, embedding in zip(
                    image_ids[i : i + 128], image_embeddings[i : i + 128]
                )
            ]
            self.index.upsert(vectors=vectors_to_upsert)
