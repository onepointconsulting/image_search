from typing import Union
from pathlib import Path
import aiohttp

from image_search.config.config import cfg
from image_search.config.log_factory import logger
from urllib.parse import urlparse


async def download_image_from_url(url: str) -> Union[Path, None]:
    parsed = urlparse(url)
    image_name = parsed.path.split("/")[-1]
    return await download_image(url, image_name)


async def download_image(url: str, image_name: str) -> Union[Path, None]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # Ensure the request was successful
            if response.status == 200:
                # Read the content of the response
                content = await response.read()
                filepath = cfg.image_storage_folder / image_name
                # Open a file in binary write mode and save the content to it
                with open(filepath, "wb") as file:
                    file.write(content)
                    return filepath
            else:
                logger.error(
                    f"Failed to download image. Status code: {response.status}"
                )
                return None
