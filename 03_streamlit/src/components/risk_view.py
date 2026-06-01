import streamlit as st
from src.services.repository import get_target_data

def risk_view():
    db_name = "PC_DBT_DB"
    schema_name = "DBT_MURA"
    table_name = "STG_CREDIT_CARD"
    
    df = get_target_data(db_name, schema_name, table_name)
    st.dataframe(df)