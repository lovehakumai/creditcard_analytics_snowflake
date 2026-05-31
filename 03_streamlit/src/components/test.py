from snowflake.snowpark.context import get_active_session
import streamlit as st 
from src.services.repository import get_target_data 
from src.services.init import store_data, load_data, init_value

def test_view():
    with st.form(key = "data_address"):
        st.header("Input table address you want")
        db_name = st.text_input("Database...")
        schema_name = st.text_input("Schema...")
        table_name = st.text_input("Table...")
    
        submit_button = st.form_submit_button(label = "Execute Query")
    
    if submit_button:
        st.info("Getting Data")
        df_pd = get_target_data(db_name, schema_name, table_name)
        st.dataframe(df_pd)