from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    openai_api_key = os.getenv("OPENAI_API_KEY")
    assert openai_api_key is not None

    openai_embeddings_model = os.getenv("OPENAI_EMBEDDINGS_MODEL")
    assert openai_embeddings_model is not None

    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/api")
    image_storage_folder_str = os.getenv("IMAGE_STORAGE_FOLDER", "./tmp/images")
    llava_model = os.getenv("LLAVA_MODEL", "llava")
    image_storage_folder = Path(image_storage_folder_str)
    if not image_storage_folder.exists():
        image_storage_folder.mkdir(parents=True)
    assert image_storage_folder.exists()

    lance_db_location = os.getenv("LANCE_DB_LOCATION", "/tmp/.lancedb")
    lance_table_image = os.getenv("LANCE_TABLE_IMAGES", "tbl_image")

    image_vector_size = int(os.getenv("IMAGE_VECTOR_SIZE", "768"))
    text_vector_size = int(os.getenv("TEXT_VECTOR_SIZE", "1536"))

    server_host = os.getenv("SERVER_HOST", "0.0.0.0")
    server_port = int(os.getenv("SERVER_PORT", "8888"))


def get_image_folder() -> Path:

    import sys

    images_path = Path("./images")
    if not images_path.exists():
        images_path = Path("./multimodal_experiments/images")
        if not images_path.exists():
            print("Cannot find the images", file=sys.stderr)
            sys.exit(1)
    return images_path


cfg = Config()
