from typing import Tuple, List

from pyarrow.lib import Schema
import pandas as pd

from image_search.vector_db.lancedb_persistence import tbl
from image_search.vector_db.imagedb_schema import (
    FIELD_IMAGE_NAME,
    FIELD_IMAGE_DESCRIPTION,
    FIELD_CREATE_TIMESTAMP,
    FIELD_UPDATE_TIMESTAMP,
)


def basic_info() -> Tuple[int, List[str]]:
    rows = tbl.count_rows()
    column_names = tbl.schema.names
    return rows, column_names


def col_info() -> List[Tuple[str, any]]:
    schema: Schema = tbl.schema
    return list(zip(schema.names, schema.types))


def get_data() -> pd.DataFrame:
    return (
        tbl.search()
        .limit(-1) # Fetches all records.
        .select(
            [
                FIELD_IMAGE_NAME,
                FIELD_IMAGE_DESCRIPTION,
                FIELD_CREATE_TIMESTAMP,
                FIELD_UPDATE_TIMESTAMP,
            ]
        )
        .to_pandas()
    )


if __name__ == "__main__":
    info = col_info()
    for i in info:
        print(i[0], i[1], type(i[1]))
    data = get_data()
    print(data.shape)
