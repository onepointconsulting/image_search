from image_search.vector_db.lancedb_persistence import tbl


if __name__ == "__main__":
    count = tbl.count_rows()
    print(f"Table {tbl} has {count} rows.")
