import streamlit as st
from src.components.test import test_view

st.title("Let me query")
st.header("#1 input the table info you wanna get")

test_view()