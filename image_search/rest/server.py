import shutil

from typing import List, Dict
from pathlib import Path
from datetime import datetime

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from tempfile import NamedTemporaryFile
from pydantic import BaseModel, Field

from image_search.vector_db.lancedb_persistence import save_image_from_path
from image_search.config.config import cfg
from image_search.config.log_factory import logger
from image_search.vector_db.text_search import text_search
from image_search.vector_db.image_search_helper import image_search
from image_search.vector_db.imagedb_schema import (
    FIELD_IMAGE_NAME,
    FIELD_IMAGE_DESCRIPTION,
)

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    with NamedTemporaryFile(delete=False) as tmp:
        tmp_path = await create_temp_file(file, tmp)
        current_timestamp = datetime.now()
        formatted_timestamp = current_timestamp.strftime("%Y%m%d_%H%M%S")
        file_copy = tmp_path.parent / f"{formatted_timestamp}_{file.filename}"
        shutil.copyfile(tmp_path, file_copy)
        output = await save_image_from_path(file_copy)
        unlink_image(tmp_path)

    return {
        "filename": file.filename,
        "temporary_file_path": tmp_path.as_posix(),
        "output": output,
    }


class SearchRequest(BaseModel):
    search: str = Field(..., description="The search expression")
    limit: int = Field(default=10, description="The amount of results")


@app.post("/search/text")
async def search_text(request: SearchRequest):
    res = text_search(request.search, request.limit)
    return search_response_adapter(res)


@app.post("/search/image")
async def search_image(
    file: UploadFile = File(...), limit: int = Form(default=10)
):
    with NamedTemporaryFile(delete=False) as tmp:
        tmp_path = await create_temp_file(file, tmp)
        res = image_search(tmp_path, limit)
        return search_response_adapter(res)


@app.post("/search/text_image")
async def create_file(file: UploadFile = File(...), search: str = Form(...)):
    limit = 5
    res_image = await search_image(file, limit=limit)
    res_text = await search_text(SearchRequest(search=search, limit=limit))

    def rank_results(res: List[Dict]):
        return {r[FIELD_IMAGE_NAME]:{**r, "rank_points": limit - i} for i, r in enumerate(res)}

    ranked_images = rank_results(res_image)
    ranked_text = rank_results(res_text)

    combined_dict = {image_name:value for image_name, value in ranked_images.items()}

    for image_name, value in ranked_text.items():
        if image_name not in combined_dict:
            combined_dict[image_name] = value
        else:
            combined_dict[image_name]['rank_points'] = combined_dict[image_name]['rank_points'] + value['rank_points']
    
    return sorted(combined_dict.values(), key=lambda x: x['rank_points'], reverse=True)


@app.get("/image/{image_name}")
async def get_image(image_name: str):
    # Define the path to the image folder
    image_path = cfg.image_storage_folder / image_name

    # Check if the image exists
    if not image_path.exists():
        raise HTTPException(status_code=404, detail=f"Image {image_name} not found")

    # Return the image as a streaming response
    return FileResponse(image_path)


def unlink_image(tmp_path: Path):
    try:
        tmp_path.unlink()
    except:
        logger.exception(f"Failed to delete {tmp_path}")


async def create_temp_file(file: UploadFile, tmp: NamedTemporaryFile):
    content = await file.read()  # Read the file content
    tmp.write(content)  # Write the file content to a temporary file
    return Path(tmp.name)  # Get the temporary file path


def search_response_adapter(res: List[Dict]):
    return [
        {
            "image_name": r[FIELD_IMAGE_NAME],
            "image_description": r[FIELD_IMAGE_DESCRIPTION],
            "url": f"/image/{r[FIELD_IMAGE_NAME]}",
            "distance": r["_distance"],
        }
        for r in res
    ]


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run(
        "image_search.rest.server:app",
        host=cfg.server_host,
        port=cfg.server_port,
        reload=True,
    )


if __name__ == "__main__":
    start()
