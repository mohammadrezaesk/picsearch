import logging
from typing import List

import numpy as np

import clip
import torch
from PIL import Image

logger = logging.getLogger(__name__)


class ClipClient:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        logger.info("Model loaded ✅")

    def batch_encode_images(self, image_paths: List[str], batch_size: int):
        image_embeddings = []
        logger.info(f"total: {len(image_paths)}")
        for i in range(0, len(image_paths), batch_size):

            batch_paths = image_paths[i : i + batch_size]  # Get the current batch
            images = []

            for img_path in batch_paths:
                image = Image.open(img_path).convert("RGB")  # Ensure RGB format
                images.append(self.preprocess(image))

            images_tensor = torch.stack(images).to(self.device)

            with torch.no_grad():
                image_features = self.model.encode_image(images_tensor)

            image_features /= image_features.norm(dim=-1, keepdim=True)

            image_embeddings.append(image_features.cpu().numpy())
            logger.info(f"one batch imported! {i}")
        return np.concatenate(image_embeddings)

    def encode_query_text(self, query_text: str):
        text = clip.tokenize([query_text]).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        return text_features.cpu().numpy()
