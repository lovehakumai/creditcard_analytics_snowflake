from snowflake.snowpark.context import get_active_session
from src.services.get_target_data import get_target_data
import pandas as pd 
import streamlit as st 

@st.cache_data(max_entries = 3)
def get_data_for_metrics_1()->pd.DataFrame:
    db_name = 'SNOWFLAKE'
    schema_name = 'ACCOUNT_USAGE'
    table_name = 'WAREHOUSE_METERING_HISTORY'
    df = get_target_data(db_name, schema_name, table_name).copy()

    return df
