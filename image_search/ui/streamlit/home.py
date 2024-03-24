import asyncio
from pathlib import Path
from typing import List, Dict
from tempfile import NamedTemporaryFile

import streamlit as st
from image_search.config.config import cfg
from image_search.ui.streamlit.navbar import nav
from image_search.vector_db.text_search import text_search
from image_search.vector_db.image_search_helper import image_search
from image_search.vector_db.imagedb_schema import (
    FIELD_IMAGE_NAME,
    FIELD_IMAGE_DESCRIPTION,
)
from image_search.vector_db.result_combiner import combine_results
from image_search.ui.streamlit.tmp_file_helper import create_temp_file

LIMIT = 10


def search_response_adapter(res: List[Dict]):
    for r in res:
        image_file: Path = cfg.image_storage_folder / r[FIELD_IMAGE_NAME]
        if image_file.exists():
            st.image(
                image_file.as_posix(),
                caption=r[FIELD_IMAGE_NAME],
                use_column_width=True,
            )
            st.markdown(r[FIELD_IMAGE_DESCRIPTION])
            if "_distance" in r:
                st.markdown(f"Distance: {r['_distance']}")


def streamlit_image_search(
    file: st.runtime.uploaded_file_manager.UploadedFile,
) -> List[Dict]:
    with NamedTemporaryFile(delete=False) as tmp:
        tmp_path = create_temp_file(uploaded_file, tmp)
        return image_search(tmp_path, LIMIT)


st.set_page_config(layout="wide")
st.header("Vector Search")

# Display the menu
nav("Home")

st.markdown(
    """This form allows you to search foro images based on an **uploaded image** or some **descriptive text**. You can also combine text and images to search the image you are looking for."""
)

with st.form(key="file_search_form"):
    # File uploader widget
    uploaded_file = st.file_uploader("Choose a file", type=cfg.supported_file_formats)
    # Text input widget for search expression
    search_expression = st.text_area("Enter search expression", height=20)

    # Submit button for the form
    submit_button = st.form_submit_button(label="Search")


if submit_button:
    # Check if either the file is uploaded or the text area is filled
    has_uploaded_file = uploaded_file is not None
    if has_uploaded_file or search_expression:
        with st.spinner("Uploading file... Please wait."):
            if has_uploaded_file and search_expression and len(search_expression) > 1:
                # Mixed search
                res_image = streamlit_image_search(uploaded_file)
                res_text = asyncio.run(text_search(search_expression, LIMIT))
                search_response_adapter(
                    combine_results(res_image, res_text, LIMIT // 2)
                )
            elif has_uploaded_file:
                # File based search
                res = streamlit_image_search(uploaded_file)
                search_response_adapter(res)
            elif search_expression:
                # Text only search
                res = asyncio.run(text_search(search_expression, LIMIT))
                search_response_adapter(res)
    else:
        # Display a message prompting the user to fill out at least one field
        st.error("Please upload an image or enter a search expression.")
