from typing import List
import asyncio

import streamlit as st
from image_search.ui.streamlit.navbar import nav
from image_search.ui.streamlit.pages.common import missing_prompt_error
from image_search.utils.download_utils import download_image_from_url
from image_search.ui.streamlit.pages.common import missing_prompt_error, display_image
from image_search.ui.streamlit.pages.common import save_image
from image_search.config.log_factory import logger
from mymidjourney_client.async_client.imagine import imagine_request
from mymidjourney_client.async_client.message_processor import message_processor
from mymidjourney_client.async_client.button import button_request
from mymidjourney_client.model.error import Error

STOP_BUTTON = "stop"

st.set_page_config(layout="wide")
st.header("Image Generation with Midjourney")

# Display the menu
nav("Generate Midjourney")

st.markdown("Here you can generate images using Midjourney")

placeholder = st.empty()

if "last_pressed" not in st.session_state:
    st.session_state.last_pressed = None

if "imagine_result" not in st.session_state:
    st.session_state.imagine_result = None

if "message_id" not in st.session_state:
    st.session_state.message_id = None

# Function to set the last pressed button
def set_last_pressed(button_name):
    st.session_state.last_pressed = button_name


def download_and_save(uri: str, prompt: str) -> bool:
    image_path = asyncio.run(download_image_from_url(uri))
    display_image(image_path, prompt)
    return save_image(image_path)


def render_buttons(buttons: List[str]):
    if not STOP_BUTTON in buttons:
        buttons.append(STOP_BUTTON)
    cols = st.columns(len(buttons))
    for i, button in enumerate(buttons):
        with cols[i]:
            if st.button(button, key=button):
                set_last_pressed(button)
    # Display the last pressed button
    if st.session_state.last_pressed is not None and st.session_state.last_pressed != STOP_BUTTON:
        last_pressed = st.session_state.last_pressed
        st.info(f"You pressed: {last_pressed}")
        logger.info(f"You pressed: {last_pressed}")
        with st.spinner("Generating and uploading file after button click ... Please wait."):
            message_id = st.session_state.message_id
            button_result = asyncio.run(button_request(message_id, last_pressed))
            if isinstance(button_result, Error):
                st.error(f"Button press returned result: {button_result.error_message}")
            else:
                button_message_result = asyncio.run(
                    message_processor(button_result.message_id)
                )
                if isinstance(button_message_result, Error):
                    st.error(
                        f"Button message returned result: {button_message_result.error_message}"
                    )
                else:
                    download_and_save(button_message_result.uri, last_pressed)
                    if last_pressed.find('U') == -1:
                        # Change the message id to generate from versions.
                        st.session_state.message_id = button_message_result.message_id
                        
            st.session_state.last_pressed = None
    elif st.session_state.last_pressed == STOP_BUTTON:
        logger.info("Stop button pressed")
        st.session_state.imagine_result = None
        st.session_state.last_pressed = None
    else:
        logger.info("No button pressed")
        


if not st.session_state.imagine_result:
    with placeholder.form(key="generate_midjourney_form"):

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
                        elif message_result is None or message_result.uri is None:
                            st.error(
                                f"Generation timed out"
                            )
                        else:
                            uri = message_result.uri
                            success = download_and_save(uri, prompt)
                            if success:
                                st.session_state["imagine_result"] = message_result
                            else:
                                st.error(f"Failed to save image from {uri}")

if st.session_state.imagine_result:
    message_result = st.session_state.imagine_result
    st.info(f"Please select buttons to select sub images or create new versions. If you want to stop, please press the 'Stop' button.")
    st.session_state.message_id = message_result.message_id
    render_buttons(message_result.buttons)
