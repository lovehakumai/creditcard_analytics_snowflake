import streamlit as st 
from snowflake.snowpark.context import get_active_session
# connect to snowflake and get data
session = get_active_session()

# get data from specific Table
@st.cache_data(max_entries = 3)
def get_target_data(db_name, schema_name, table_name):
    sql = "SELECT * FROM ?.?.?"
    df_pd = session.sql(sql, params=[1: db_name, 2: schema_name, 3: table_name])
    
    return df_pd 