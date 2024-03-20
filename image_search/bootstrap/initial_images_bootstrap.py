from image_search.vector_db.lancedb_persistence import save_image, tbl

if __name__ == "__main__":

    import asyncio
    import sys
    from pathlib import Path

    from image_search.config.config import get_image_folder
    from image_search.service.conversion_service import (
        create_image_embeddings,
    )

    async def bootstrap_images():
        images_path = get_image_folder()
        if len(sys.argv) > 1:
            images_path = Path(sys.argv[1])
            assert images_path.exists(), f"Path {images_path} does not exist."

        async for image_data in create_image_embeddings(images_path):
            save_image(image_data)
            print("Saved", image_data.file_name)

    asyncio.run(bootstrap_images())

    count = tbl.count_rows()
    print(f"Table {tbl} has {count} rows.")
