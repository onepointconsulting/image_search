from typing import List, Union, Dict
from pathlib import Path

from enum import StrEnum
import lancedb
import numpy as np

from image_search.config.log_factory import logger
from image_search.model.image_data import ImageData
from image_search.model.error import Error, ErrorCode
from image_search.vector_db.imagedb_schema import schema
from image_search.model.image_data import convert_to_pyarrow
from image_search.config.config import cfg
from image_search.vector_db.imagedb_schema import (
    FIELD_IMAGE_VECTOR,
    FIELD_IMAGE_NAME,
    FIELD_TEXT_VECTOR,
    FIELD_IMAGE_DESCRIPTION,
    FIELD_CREATE_TIMESTAMP,
    FIELD_UPDATE_TIMESTAMP,
)
from image_search.service.conversion_service import (
    convert_single_image,
)
from image_search.utils.file_utils import unlink_file


class DISTANCE(StrEnum):
    EUCLIDEAN = "l2"
    COSINE = "cosine"
    DOT = "dot"


def execute_knn_search(
    embedding: List[float],
    vector_column_name: str,
    limit: int = 10,
    distance: str = DISTANCE.EUCLIDEAN,
) -> List[Dict]:
    return (
        tbl.search(
            embedding, query_type="vector", vector_column_name=vector_column_name
        )
        .metric(distance)
        .limit(limit)
        .to_list()
    )


def init_image_vector_table() -> lancedb.table.LanceTable:
    db = lancedb.connect(cfg.lance_db_location)
    table_name = cfg.lance_table_image
    try:
        return db.open_table(table_name)
    except FileNotFoundError as e:
        logger.warning("Could not open database. It does not exist.")
        return db.create_table(table_name, schema=schema)


tbl = init_image_vector_table()


def sql_escape(text: str) -> str:
    return text.replace("'", "''")


def convert_vec_to_literal(float_list: List[float]) -> List[str]:
    return [str(v) for v in float_list]


def save_image(image_data: ImageData, ignore_update: bool = False) -> bool:
    results = execute_knn_search(image_data.image_embedding, FIELD_IMAGE_VECTOR, 1)
    image_available = False
    if len(results) > 0:
        first_result = results[0]
        image_available = np.array_equal(
            first_result[FIELD_IMAGE_VECTOR], image_data.image_embedding
        )
    if not image_available:  # insert
        logger.info("Creating %s", image_data.file_name)
        pa_table = convert_to_pyarrow(image_data, None)
        tbl.add(pa_table)
        return True
    else:  # update
        logger.info("Updating %s", image_data.file_name)
        first_result = results[0]
        if ignore_update == False:
            create_timestamp = first_result[FIELD_CREATE_TIMESTAMP]
            pa_table = convert_to_pyarrow(image_data, create_timestamp)

            single_value = {
                FIELD_TEXT_VECTOR: convert_vec_to_literal(
                    first_result[FIELD_TEXT_VECTOR]
                ),
                FIELD_IMAGE_DESCRIPTION: sql_escape(
                    first_result[FIELD_IMAGE_DESCRIPTION]
                ),
                FIELD_IMAGE_VECTOR: convert_vec_to_literal(
                    first_result[FIELD_IMAGE_VECTOR]
                ),
                FIELD_UPDATE_TIMESTAMP: first_result[FIELD_UPDATE_TIMESTAMP],
            }
            filter_expression = (
                f"{FIELD_IMAGE_NAME} = '{first_result[FIELD_IMAGE_NAME]}'"
            )
            if image_data.image_path:
                # The file was uploaded again. Keep the old file to avoid dups.
                unlink_file(cfg.image_storage_folder/image_data.file_name)
            tbl.update(where=filter_expression, values=single_value)
        return False


async def save_image_from_path(image_path: Path) -> Union[bool, Error]:
    if not image_path.exists():
        return Error(
            code=ErrorCode.NOT_FOUND,
            message=f"Could not find original image path: {image_path}",
        )
    image_data = await convert_single_image(image_path)
    if image_data is None:
        return Error(
            ErrorCode.DESCRIPTION_MISSING,
            f"Image description is missing for {image_path}",
        )
    return save_image(image_data)
