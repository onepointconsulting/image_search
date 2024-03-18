import streamlit as st
from streamlit_option_menu import option_menu

# Define the pages and their file paths
pages = {"Home": f"home.py", "Upload": f"pages/upload.py"}

# Create a list of the page names
page_list = list(pages.keys())


def nav(current_page=page_list[0]):
    with st.sidebar:
        p = option_menu(
            "Main Menu",
            page_list,
            default_index=page_list.index(current_page),
            orientation="vertical",
        )

        if current_page != p:
            st.switch_page(pages[p])
