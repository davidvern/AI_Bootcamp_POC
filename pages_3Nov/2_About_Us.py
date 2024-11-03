# pages/2_About_Us.py
import streamlit as st
from pathlib import Path

st.logo("data/Information_page/PUB_logo.png")

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

intro_markdown = read_markdown_file('data/Information_page/About_Us_WriteUp.md')
st.markdown(intro_markdown, unsafe_allow_html=True)