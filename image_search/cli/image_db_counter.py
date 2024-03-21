from image_search.vector_db.lancedb_info import basic_info


if __name__ == "__main__":
    count, names = basic_info()
    print(f"Table has {count} rows.")
    print("Columns", names)
