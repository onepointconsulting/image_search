from pathlib import Path

from image_search.config.log_factory import logger


def unlink_file(tmp_path: Path):
    if tmp_path is not None:
        try:
            tmp_path.unlink()
        except:
            logger.exception(f"Failed to delete {tmp_path}")
