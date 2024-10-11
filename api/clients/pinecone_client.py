import logging

from pinecone import Pinecone
import config

logger = logging.getLogger(__name__)


class PineconeClient:
    def __init__(self):
        pc = Pinecone(api_key=config.PINECONE_API_KEY)
        self.index = pc.Index(
            name=config.PINECONE_IMAGE_INDEX_NAME, host=config.PINECONE_HOST_URL
        )
        logger.info("Pinecone connected ✅")

    def upsert_image(self, image_embeddings, image_ids):
        if len(image_embeddings) != len(image_ids):
            raise ValueError("Image embeddings must have same length")
        for i in range(0, len(image_embeddings), 128):
            vectors_to_upsert = [
                (image_id, embedding.tolist())
                for image_id, embedding in zip(
                    image_ids[i : i + 128], image_embeddings[i : i + 128]
                )
            ]
            self.index.upsert(vectors=vectors_to_upsert)

    def search_by_query(self, text_embedding, count: int):
        return self.index.query(vector=text_embedding.tolist(), top_k=count)
