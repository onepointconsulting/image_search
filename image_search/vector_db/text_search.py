from typing import List, Dict
from image_search.vector_db.lancedb_persistence import tbl
from image_search.vector_db.imagedb_schema import (
    FIELD_TEXT_VECTOR,
    FIELD_IMAGE_DESCRIPTION,
)
from image_search.service.openai_embeddings import create_text_embeddings
from image_search.vector_db.lancedb_persistence import execute_knn_search, DISTANCE


def text_search(
    image_description: str, limit: int = 10, distance: str = DISTANCE.EUCLIDEAN
) -> List[Dict]:
    embedding = create_text_embeddings(image_description)
    res = execute_knn_search(embedding, FIELD_TEXT_VECTOR, limit, distance)
    return res


if __name__ == "__main__":

    def test_list_text_vectors():
        for i, img in enumerate(tbl.to_pandas()[FIELD_TEXT_VECTOR].to_numpy()):
            print(i, img)

    def search_tester(search: str):
        print("Searching for: ", search)
        res = text_search(search, 3, DISTANCE.DOT)
        for dic in res:
            print(dic[FIELD_IMAGE_DESCRIPTION])
            print("\n******************************************\n")

    def test_text_search_2():
        search_tester("ritualistic or ceremonial gathering.")

    def test_text_search_3():
        search_tester("ancient temple interior with intricate stonework")

    def test_text_search_4():
        search_tester(
            "a person standing in front of a group of people who appear to be part of a ritualistic or ceremonial gathering"
        )

    def test_text_search_5():
        search_tester("adding to the atmosphere of mystery and intrigue")

    def test_text_search_young_woman():
        search_tester("young woman")

    def test_text_transformers():
        search_tester("transformer robots")

    test_text_search_3()
