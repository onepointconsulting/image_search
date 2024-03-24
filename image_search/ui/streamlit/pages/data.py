import streamlit as st

from image_search.ui.streamlit.navbar import nav
from image_search.vector_db.lancedb_info import get_data
from image_search.ui.streamlit.navbar import Page

st.set_page_config(layout="wide")
st.header("Data")

# Display the menu
nav(Page.DATA)

image_metadata = get_data()

st.markdown(
    f"""Here you can see data contained in this database.""")

st.dataframe(image_metadata)
