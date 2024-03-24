from typing import List, Dict

from pathlib import Path
from image_search.service.image_embeddings.embedding_query import get_image_emb
from image_search.vector_db.lancedb_persistence import DISTANCE, execute_knn_search
from image_search.vector_db.imagedb_schema import (
    FIELD_IMAGE_VECTOR,
    FIELD_IMAGE_NAME,
)


def image_search(
    image_path: Path, limit: int = 10, distance: str = DISTANCE.EUCLIDEAN
) -> List[Dict]:
    embedding = get_image_emb(image_path)
    return execute_knn_search(embedding, FIELD_IMAGE_VECTOR, limit, distance)


if __name__ == "__main__":
    from image_search.config.config import get_image_folder

    def search_tester(image_path: Path):
        print("Searching for: ", image_path)
        res = image_search(image_path, 3, DISTANCE.DOT)
        for dic in res:
            print(dic[FIELD_IMAGE_NAME])
            print("\n******************************************\n")

    images_path = get_image_folder()
    image_list = list(images_path.glob("*.png"))
    if len(image_list) > 0:
        first_image = image_list[0]
        print(f"== {first_image} ==")
        search_tester(first_image)
