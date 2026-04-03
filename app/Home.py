import streamlit as st

from app.components.layout import render_home
from app.utils.theme import inject_theme

st.set_page_config(
    page_title="WOD Block Builder",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme()
render_home()
