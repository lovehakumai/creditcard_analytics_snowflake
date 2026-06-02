import streamlit as st
from src.services.get_target_data import get_target_data
import pandas as pd 
import streamlit as st 

@st.cache_data(max_entries = 3)
def get_data_for_metrics_2()->pd.DataFrame:
    db_name = "PC_DBT_DB"
    schema_name = "DBT_MURA"
    table_name = "FCT_CREDIT_RISK_MART"
    
    df = get_target_data(db_name, schema_name, table_name).copy()
    return df 
    