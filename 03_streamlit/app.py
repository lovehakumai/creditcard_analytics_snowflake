import os 
import sys
import streamlit as st

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.components.test import test_view

st.title("Let me query")
st.header("#1 input the table info you wanna get")

test_view()