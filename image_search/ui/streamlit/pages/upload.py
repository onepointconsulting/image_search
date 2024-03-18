import shutil
import asyncio
from tempfile import NamedTemporaryFile

import streamlit as st
from image_search.ui.streamlit.navbar import nav
from image_search.ui.streamlit.tmp_file_helper import create_temp_file
from image_search.utils.time_utils import generate_file_timestamp
from image_search.vector_db.lancedb_persistence import save_image_from_path
from image_search.utils.file_utils import unlink_file
from image_search.model.error import Error
from image_search.config.config import cfg


st.set_page_config(layout="wide")
st.header("Image Upload")

# Display the menu
nav("Upload")

st.markdown(
    """This page allows you to upload an image to the vector database."""
)

with st.form(key="image_upload_form"):
    # File uploader widget
    uploaded_file = st.file_uploader(
        "Choose a file", type=cfg.supported_file_formats
    )

    # Submit button for the form
    submit_button = st.form_submit_button(label="Upload")

if submit_button:
    if uploaded_file is None:
        # Display a message prompting the user to fill out the upload file
        st.error("Please upload an image")        
    else:
        tmp_path = None
        with NamedTemporaryFile(delete=False) as tmp:
            tmp_path = create_temp_file(uploaded_file, tmp)
            formatted_timestamp = generate_file_timestamp()
            file_copy = tmp_path.parent / f"{formatted_timestamp}_{uploaded_file.name}"
            print("file_copy", file_copy)
            shutil.copyfile(tmp_path, file_copy)
            print("file_copy exists", file_copy.exists())
            output = asyncio.run(save_image_from_path(file_copy))

            if type(output) == Error:
                st.error(f"Image upload failed due to {output.message}")
            else:
                st.info(f"Image {uploaded_file.name} successfully {'created' if output else 'updated'}")

        unlink_file(tmp_path)

