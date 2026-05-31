import streamlit as st 

def store_data(key):
    st.session_state[key] = st.session_state['_' + key]
def load_data(key):
    st.session_state['_' + key] = st.session_state[key]
def init_value(key, init_value):
    if key not in st.session_state:
        st.session_state[key] = init_value