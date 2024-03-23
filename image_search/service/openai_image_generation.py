from typing import List
from pathlib import Path
from enum import StrEnum
from urllib.parse import urlparse

from openai import AsyncOpenAI

from image_search.config.config import cfg
from image_search.utils.download_utils import download_image

client = AsyncOpenAI()


class Sizes(StrEnum):
    SQUARE = "1024x1024"
    PORTRAIT = "1024x1792"
    LANDSCAPE = "1792x1024"


async def generate_image(
    prompt: str, number_of_images: int = 1, size: Sizes = Sizes.SQUARE
) -> List[Path]:
    response = await client.images.generate(
        model=cfg.openai_image_model,
        prompt=prompt,
        n=number_of_images,  # Number of images to generate
        size=size,  # Size of the generated image,
        response_format="url",
    )
    urls = [image.url for image in response.data]
    downloaded_images = []
    for url in urls:
        parsed = urlparse(url)
        image_name = parsed.path.split("/")[-1]
        downloaded_image = await download_image(url, image_name)
        if downloaded_image is not None:
            downloaded_images.append(downloaded_image)
    return downloaded_images


if __name__ == "__main__":

    import asyncio

    images = asyncio.run(
        generate_image(
            "Generate an image of a futuristic spaceship flying past the planet of Saturn"
        )
    )
    for im in images:
        print(im)
