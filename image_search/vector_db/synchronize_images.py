from image_search.config.config import cfg
from image_search.vector_db.lancedb_persistence import tbl

def cleanup_image_folder():
    for file in cfg.image_storage_folder.glob("*"):
        name = file.name
        res = tbl.search().where(f"image_name = '{name}'", prefilter=True).to_list()
        if len(res) == 0:
            print(f"Cannot find {file.name}")
            file.unlink()


def cleanup_db(limit=1000):
    res = tbl.search().limit(limit).to_list()
    files = set([f.name for f in list(cfg.image_storage_folder.glob("*"))])
    for row in res:
        image_name = row['image_name']
        if image_name not in files:
            print(f"Image {image_name} not available in folder.")
            tbl.delete(where=f"image_name = '{image_name}'")