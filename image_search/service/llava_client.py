from typing import Union, List
from pathlib import Path

import aiohttp

from image_search.config.config import cfg
from image_search.error import Error
from image_search.image_encoder_decoder import encode_image


async def describe(
    image_path: Path, prompt: str = "What is in this picture?"
) -> Union[str, Error]:
    data = {
        "model": "llava",
        "prompt": prompt,
        "stream": False,
        "images": [encode_image(image_path)],
    }
    generate_url = f"{cfg.ollama_base_url}/generate"
    return await handle_post_call(data, generate_url, "response")


async def embeddings(image_path: Path, description: str) -> Union[List[float], Error]:
    data = {"model": "llava", "prompt": description, "images": encode_image(image_path)}
    embeddings_url = f"{cfg.ollama_base_url}/embeddings"
    return await handle_post_call(data, embeddings_url, "embedding")


async def handle_post_call(
    data: dict, url: str, key: str
) -> Union[Union[List[float], str], Error]:
    """
    Generates a description for an image at the given path using a specified prompt.

    Args:
        image_path (Path): The filesystem path to the image to describe.
        prompt (str): The prompt to guide the description generation.

    Returns:
        Union[str, Error]: The generated description or an Error object if the request failed.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            if resp.status >= 200 and resp.status < 300:
                json_res = await resp.json()
                if key in json_res:
                    return json_res[key]
                else:
                    return Error(code=resp.status, message="Failed to extract response")
            else:
                return Error(code=resp.status, message=await resp.text())


if __name__ == "__main__":
    import sys
    import asyncio

    images_path = Path("./images")
    if not images_path.exists():
        images_path = Path("./multimodal_experiments/images")
        if not images_path.exists():
            print("Cannot find the images", file=sys.stderr)
            sys.exit(1)

    for im in images_path.glob("*.png"):
        print(f""" ===== {im.name} =====""")
        description = asyncio.run(describe(im))
        print(description)
        print()
        if description is not None:
            embs = asyncio.run(embeddings(im, description))
            if type(embs) != Error:
                print("Embeddings length: ", len(embs))
