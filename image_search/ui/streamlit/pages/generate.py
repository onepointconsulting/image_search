import asyncio

import streamlit as st

from image_search.config.log_factory import logger
from image_search.ui.streamlit.navbar import nav
from image_search.service.openai_image_generation import Sizes, generate_image
from image_search.vector_db.lancedb_persistence import save_image_from_path
from image_search.utils.file_utils import unlink_file

st.set_page_config(layout="wide")
st.header("Image Generation")

# Display the menu
nav("Generate")

st.markdown("Here you can generate images using DALL-E and save them directly in the vector database.")

with st.form(key="generate_form"):
    
    # Text input widget for search expression
    prompt = st.text_area("Enter image prompt", height=20)

    dropdown_selection = st.selectbox('Choose the image format:', [Sizes.SQUARE, Sizes.PORTRAIT, Sizes.LANDSCAPE])

    # Submit button for the form
    submit_button = st.form_submit_button(label="Generate")

if submit_button:
    if prompt is None or len(prompt) < 5:
        st.error("The image prompt should have at least 5 characters")
    else:
        selected_format = dropdown_selection
        with st.spinner("Generating and uploading file... Please wait."):
            downloaded_images = asyncio.run(generate_image(prompt, 1, selected_format))
            for image in downloaded_images:
                st.info(f"Generated {image.name}")
                st.image(
                    image.as_posix(),
                    caption=prompt,
                    use_column_width=True,
                )
                try:
                    asyncio.run(save_image_from_path(image))
                    st.info(f"Created {image.name}")
                except:
                    logger.exception("Failed to create image")
                    st.info(f"Failed to import {image.name} to vector database.")
                finally:
                    unlink_file(image)

        
        
