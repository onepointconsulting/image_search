from typing import List
from openai import OpenAI

from image_search.config.config import cfg

client = OpenAI()


def openai_create_text_embeddings(text: str) -> List[float]:
    return (
        client.embeddings.create(input=[text], model=cfg.openai_embeddings_model)
        .data[0]
        .embedding
    )


if __name__ == "__main__":
    res = openai_create_text_embeddings("This is a sime text.")
    print(len(res))
