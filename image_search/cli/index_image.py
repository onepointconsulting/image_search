from pathlib import Path
import sys

from image_search.config.log_factory import logger
from image_search.vector_db.lancedb_persistence import save_image_from_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Please specify the image paths")
        sys.exit(1)

    for path_str in sys.argv[1:]:
        logger.info("Processing %s", path_str)
        image_path = Path(path_str)
        if not image_path.exists():
            logger.warn("Image %s does not exist", image_path)
        else:
            save_image_from_path(image_path)
