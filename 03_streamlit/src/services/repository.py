import streamlit as st 
from snowflake.snowpark.context import get_active_session
# connect to snowflake and get data
session = get_active_session()

# get data from specific Table
@st.cache_data(max_entries = 3)
def get_target_data(db_name, schema_name, table_name):
    df_pd = session.table([db_name, schema_name, table_name]).to_pandas()
    return df_pd 