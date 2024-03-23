from typing import Tuple, List

from pyarrow.lib import Schema

from image_search.vector_db.lancedb_persistence import tbl


def basic_info() -> Tuple[int, List[str]]:
    rows = tbl.count_rows()
    column_names = tbl.schema.names
    return rows, column_names


def col_info() -> List[Tuple[str, any]]:
    schema: Schema = tbl.schema
    return list(zip(schema.names, schema.types))


if __name__ == "__main__":
    info = col_info()
    for i in info:
        print(i[0], i[1], type(i[1]))
