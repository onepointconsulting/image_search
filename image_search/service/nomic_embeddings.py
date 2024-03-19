from typing import List, Union

import aiohttp

from image_search.config.config import cfg
from image_search.config.log_factory import logger


async def nomic_create_text_embeddings(prompt: str) -> Union[List[float], None]:
    url = f"{cfg.ollama_base_url}/embeddings"
    data = {"model": cfg.nomic_embed_model, "prompt": prompt}
    print(data)

    # Use aiohttp.ClientSession for making HTTP requests
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            # Check if the request was successful
            if response.status == 200:
                response_json = await response.json()
                # Extract the embeddings key
                embeddings = response_json.get("embedding")
                return embeddings
            else:
                logger.error(f"Error: Received response code {response.status}")
                return None


if __name__ == "__main__":
    import asyncio

    embeddings = asyncio.run(
        nomic_create_text_embeddings(
            "is a large context length text encoder that surpasses OpenAI"
        )
    )

    assert isinstance(embeddings, list)
    print("size", len(embeddings))
