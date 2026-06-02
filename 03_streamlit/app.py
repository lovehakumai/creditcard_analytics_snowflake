import os 
import sys
import streamlit as st

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.components.title_view import title_view
from src.components.layout1_view import layout1_view
from src.components.layout2_view import layout2_view

title_view()
st.markdown('---')
st.header('01-SNOWFLAKE COST CHARTS')
layout1_view()
st.markdown('---')
st.header('02-MONITOR RISKY CUSTOMERS')
layout2_view()
