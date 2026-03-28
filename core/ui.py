import base64
from pathlib import Path
import streamlit as st


def render_logo(center: bool = True, width: int = 300) -> None:
    logo_path = Path("assets/logo.png")
    logo_base64 = base64.b64encode(logo_path.read_bytes()).decode("utf-8")

    justify = "center" if center else "flex-start"

    st.markdown(
        f"""
        <div class="logo-container" style="justify-content: {justify};">
            <img src="data:image/png;base64,{logo_base64}" class="logo-img" alt="Dormify Logo" style="max-width:{width}px;">
        </div>
        """,
        unsafe_allow_html=True,
    )