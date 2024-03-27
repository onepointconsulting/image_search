import asyncio

from pathlib import Path
import streamlit as st

from image_search.config.log_factory import logger
from image_search.vector_db.lancedb_persistence import save_image_from_path
from image_search.utils.file_utils import unlink_file


def missing_prompt_error():
    st.error("The image prompt should have at least 5 characters")


def display_image(image: Path, prompt: str):
    st.info(f"Generated {image.name}")
    st.image(
        image.as_posix(),
        caption=prompt,
        use_column_width=True,
    )


def save_image(image: Path) -> bool:
    try:
        asyncio.run(save_image_from_path(image))
        st.info(f"Created {image.name}")
        return True
    except:
        logger.exception("Failed to create image")
        st.info(f"Failed to import {image.name} to vector database.")
        return False
    finally:
        unlink_file(image)
