import streamlit as st

from image_search.ui.streamlit.navbar import nav
from image_search.vector_db.lancedb_persistence import tbl

st.set_page_config(layout="wide")
st.header("Database stats")

# Display the menu
nav("Upload")

st.markdown(
    f"""Here are some informations about the image database:
- Number of rows: {tbl.count_rows()}
"""
)