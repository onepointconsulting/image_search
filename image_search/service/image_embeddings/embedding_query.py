from typing import List

from pathlib import Path
import io

import clip
import numpy as np
import torch
from PIL import Image as pimage

from image_search.config.log_factory import logger


model, preprocess = clip.load("ViT-L/14", device="cpu", jit=True)


def img_to_stream(path: Path):
    assert path.exists(), f"Path {path} does not exist"
    img_stream = io.BytesIO(path.read_bytes())
    return img_stream


def convert_to_list(array: np.ndarray) -> List[float]:
    return array.cpu().detach().numpy().astype("float32")[0].tolist()


def get_image_emb(path: Path) -> List[float]:
    """
    Generates an embedding for an image at a specified path.

    This function processes an image through the pre-loaded CLIP model to
    generate a normalized embedding vector. The embedding is then converted
    to a list of floats. Logging is used to track the shape of the embedding
    before and after normalization.

    Parameters:
    - path (Path): The file path to the image for which the embedding is generated.

    Returns:
    - List[float]: A normalized embedding of the image as a list of floats.
    """
    with torch.no_grad():
        image = pimage.open(img_to_stream(path))
        image_emb = model.encode_image(preprocess(image).unsqueeze(0).to("cpu"))
        logger.info(f"Shape: {image_emb.shape}")
        image_emb /= image_emb.norm(dim=-1, keepdim=True)
        logger.info(f"Shape normalized: {image_emb.shape}")
        return convert_to_list(image_emb)


def get_text_emb(text: str) -> np.ndarray:
    with torch.no_grad():
        text_emb = model.encode_text(clip.tokenize([text], truncate=True).to("cpu"))
        text_emb /= text_emb.norm(dim=-1, keepdim=True)
        return convert_to_list(text_emb)


if __name__ == "__main__":

    import sys

    images_path = Path("./images")
    if not images_path.exists():
        images_path = Path("./multimodal_experiments/images")
        if not images_path.exists():
            print("Cannot find the images", file=sys.stderr)
            sys.exit(1)

    first_image = list(images_path.glob("*.png"))[0]
    logger.info(f"Processing: {first_image}")
    img_embedding = get_image_emb(first_image)
    logger.info(f"img_embedding final shape: {len(img_embedding)}")
    logger.info(f"Embedding type: {type(img_embedding)}")
    text_embedding = get_text_emb(
        "Image of transformer having a conversation with a human seated on a chair."
    )
    logger.info(f"text_embedding final shape: {len(text_embedding)}")
