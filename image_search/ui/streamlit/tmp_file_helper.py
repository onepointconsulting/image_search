from pathlib import Path

from tempfile import NamedTemporaryFile

import streamlit as st


def create_temp_file(
    file: st.runtime.uploaded_file_manager.UploadedFile, tmp: NamedTemporaryFile
) -> Path:
    content = file.getbuffer()
    tmp.write(content)
    return Path(tmp.name)
