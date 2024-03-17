from pathlib import Path
from typing import Optional

import datetime
from typing import List
from dataclasses import dataclass

import pyarrow as pa
from image_search.vector_db.imagedb_schema import (
    FIELD_IMAGE_VECTOR,
    FIELD_TEXT_VECTOR,
    FIELD_IMAGE_NAME,
    FIELD_IMAGE_DESCRIPTION,
    FIELD_CREATE_TIMESTAMP,
    FIELD_UPDATE_TIMESTAMP,
)
from image_search.config.config import cfg


@dataclass
class ImageData:
    file_name: str
    description: str
    image_embedding: List[float]
    text_embedding: List[float]
    image_path: Optional[Path] = None


def convert_to_pyarrow(
    image_data: ImageData, create_timestamp: Optional[int]
) -> pa.lib.Table:
    current_timestamp = int(datetime.datetime.now().timestamp() * 1_000)
    vector_size = cfg.image_vector_size
    elements = [
        pa.array([image_data.image_embedding], pa.list_(pa.float32(), vector_size)),
        pa.array(
            [image_data.text_embedding], pa.list_(pa.float32(), cfg.text_vector_size)
        ),
        pa.array([image_data.file_name]),
        pa.array([image_data.description]),
    ]

    if create_timestamp:
        elements.append(pa.array([create_timestamp]))
    else:
        elements.append(pa.array([current_timestamp]))
    elements.append(pa.array([current_timestamp]))

    pa_table = pa.Table.from_arrays(
        elements,
        [
            FIELD_IMAGE_VECTOR,
            FIELD_TEXT_VECTOR,
            FIELD_IMAGE_NAME,
            FIELD_IMAGE_DESCRIPTION,
            FIELD_CREATE_TIMESTAMP,
            FIELD_UPDATE_TIMESTAMP,
        ],
    )
    return pa_table
