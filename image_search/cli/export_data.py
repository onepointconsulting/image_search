import pandas as pd

from image_search.vector_db.lancedb_persistence import tbl
from image_search.config.config import cfg

if __name__ == "__main__":
    df = tbl.to_pandas()
    df.to_csv("images_data.csv")
