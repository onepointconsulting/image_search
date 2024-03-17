import asyncio
import uuid
import shutil

from typing import Iterator, Union
from pathlib import Path

from image_search.config.config import cfg
from image_search.config.log_factory import logger
from image_search.image_embeddings.embedding_query import get_image_emb
from image_search.model.image_data import ImageData
from image_search.llava_client import describe
from image_search.service.openai_embeddings import create_text_embeddings
from image_search.model.error import Error, ErrorCode


async def create_image_embeddings(
    images_path: Path, glob_expression: str = "*.png"
) -> Iterator[ImageData]:
    if not images_path.exists():
        return
    for im in images_path.glob(glob_expression):
        yield await convert_single_image(im)


async def convert_single_image(im: Path) -> Union[ImageData, None]:

    logger.info(f""" ===== {im.name} =====""")

    new_image_path = copy_image_to_images_folder(im)
    if not new_image_path.exists():
        return Error(
            code=ErrorCode.NOT_FOUND,
            message=f"Could not find new image path: {im}",
        )

    description = await describe(im)
    logger.info(f"{description}\n")

    if description is not None:
        image_embedding = get_image_emb(im)
        embedding = create_text_embeddings(description)
        return ImageData(
            new_image_path.name, description, image_embedding, embedding, new_image_path
        )
    else:
        return None


def copy_image_to_images_folder(im: Path) -> Path:
    prefix = str(uuid.uuid4())
    image_name = f"{prefix}_{im.name}"
    new_image = cfg.image_storage_folder / image_name
    shutil.copyfile(im, new_image)
    return new_image


if __name__ == "__main__":

    from image_search.model.image_data import convert_to_pyarrow
    from image_search.config.config import get_image_folder

    images_path = get_image_folder()

    for image_data in create_image_embeddings(images_path):
        res = convert_to_pyarrow(image_data, False)
        print(type(res))
        break
