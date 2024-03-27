import asyncio

import streamlit as st
from image_search.ui.streamlit.navbar import nav
from image_search.ui.streamlit.pages.common import missing_prompt_error
from image_search.utils.download_utils import download_image_from_url
from image_search.ui.streamlit.pages.common import missing_prompt_error, display_image
from mymidjourney_client.async_client.imagine import imagine_request
from mymidjourney_client.async_client.message_processor import message_processor
from mymidjourney_client.model.error import Error
from image_search.ui.streamlit.pages.common import save_image

st.set_page_config(layout="wide")
st.header("Image Generation with Midjourney")

# Display the menu
nav("Generate Midjourney")

st.markdown("Here you can generate images using Midjourney")

with st.form(key="generate_midjourney_form"):

    # Text input widget for search expression
    prompt = st.text_area("Enter image prompt", height=20)

    # Submit button for the form
    submit_button = st.form_submit_button(label="Generate")

    if submit_button:
        if prompt is None or len(prompt) < 5:
            missing_prompt_error()
        else:
            with st.spinner("Generating and uploading file... Please wait."):
                imagine_result = asyncio.run(imagine_request(prompt))
                if isinstance(imagine_result, Error):
                    st.error(f"Imagine call failed: {imagine_result.error_message}")
                else:
                    message_result = asyncio.run(
                        message_processor(imagine_result.message_id)
                    )
                    if isinstance(message_result, Error):
                        st.error(
                            f"Message for imagine call failed: {message_result.error_message}"
                        )
                    else:
                        uri = message_result.uri
                        image_path = asyncio.run(download_image_from_url(uri))
                        display_image(image_path, prompt)
                        success = save_image(image_path)
                        if success:
                            pass
