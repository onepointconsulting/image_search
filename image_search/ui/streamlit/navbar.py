from enum import StrEnum

import streamlit as st

from streamlit_option_menu import option_menu


class Page(StrEnum):
    HOME = "Home"
    UPLOAD = "Upload"
    GENERATE = "Generate"
    STATS = "Stats"
    DATA = "Data"


# Define the pages and their file paths
pages = {
    Page.HOME: f"home.py",
    Page.UPLOAD: f"pages/upload.py",
    Page.GENERATE: f"pages/generate.py",
    Page.DATA: f"pages/data.py",
    Page.STATS: f"pages/stats.py",
}

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
