import unittest

from image_search.service.conversion_service import copy_image_to_images_folder
from image_search.config.config import get_image_folder


class TestDBModel(unittest.TestCase):
    def test_image_copy(self):
        images_path = get_image_folder()
        images_2 = images_path.parent / "images_2"
        assert images_2.exists()
        images_to_copy = list(images_2.glob("*"))
        assert len(images_to_copy) > 0
        image_to_copy = images_to_copy[0]
        assert image_to_copy.exists()
        copied = copy_image_to_images_folder(image_to_copy)
        assert copied.exists()
        copied.unlink()
        assert copied.exists() == False

    def test_image_copy_2(self):
        images_path = get_image_folder()
        images_2 = images_path.parent / "images_2"
        image_to_copy = images_2/"DALL·E 2024-03-17 19.36.03 - An abstract representation of the concept of economy of time, featuring a large, vintage clock in the center, its hands moving rapidly. Surrounding th.webp"
        assert image_to_copy.exists()
        copied = copy_image_to_images_folder(image_to_copy)
        assert copied.exists()
        copied.unlink()
        assert copied.exists() == False


if __name__ == "__main__":
    unittest.main()
