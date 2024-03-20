import pandas as pd

from image_search.vector_db.synchronize_images import cleanup_image_folder, cleanup_db

if __name__ == "__main__":
    cleanup_image_folder()
    cleanup_db()