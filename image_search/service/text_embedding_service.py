from typing import List
from image_search.config.config import cfg
from image_search.service.openai_embeddings import openai_create_text_embeddings
from image_search.service.nomic_embeddings import nomic_create_text_embeddings


async def create_text_embeddings(text: str) -> List[float]:
    if cfg.openai_embeddings_model:
        return openai_create_text_embeddings(text)
    else:
        return await nomic_create_text_embeddings(text)
