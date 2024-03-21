import streamlit as st

from image_search.ui.streamlit.navbar import nav
from image_search.vector_db.lancedb_persistence import tbl
from image_search.vector_db.lancedb_info import basic_info

st.set_page_config(layout="wide")
st.header("Database stats")

# Display the menu
nav("Stats")

count, column_names = basic_info()

st.markdown(
    f"""Here are some informations about the image database:
- Number of rows: {count}
- Number of columns: {len(column_names)}

Here are the columns names:
- {"- ".join([c + "\n" for c in column_names])}
"""
)


