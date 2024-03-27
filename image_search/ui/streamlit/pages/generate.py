import asyncio

import streamlit as st

from image_search.ui.streamlit.navbar import nav
from image_search.service.openai_image_generation import Sizes, generate_image
from image_search.ui.streamlit.pages.common import save_image
from image_search.ui.streamlit.pages.common import missing_prompt_error, display_image


st.set_page_config(layout="wide")
st.header("Image Generation")

# Display the menu
nav("Generate")

st.markdown(
    "Here you can generate images using DALL-E and save them directly in the vector database."
)

with st.form(key="generate_form"):

    # Text input widget for search expression
    prompt = st.text_area("Enter image prompt", height=20)

    dropdown_selection = st.selectbox(
        "Choose the image format:", [Sizes.SQUARE, Sizes.PORTRAIT, Sizes.LANDSCAPE]
    )

    # Submit button for the form
    submit_button = st.form_submit_button(label="Generate")

if submit_button:
    if prompt is None or len(prompt) < 5:
        missing_prompt_error()
    else:
        selected_format = dropdown_selection
        with st.spinner("Generating and uploading file... Please wait."):
            downloaded_images = asyncio.run(generate_image(prompt, 1, selected_format))
            for image in downloaded_images:
                display_image(image, prompt)
                save_image(image)
