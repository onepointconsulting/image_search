from typing import Tuple, List

from image_search.vector_db.lancedb_persistence import tbl

def basic_info() -> Tuple[int, List[str]]:
    rows = tbl.count_rows()
    column_names = tbl.schema.names
    return rows, column_names