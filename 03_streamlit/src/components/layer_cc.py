import streamlit as st 
from src.models.get_data_for_metrics_2 import get_data_for_metrics_2

def layer_cc():
    df = get_data_for_metrics_2()
    summary_df = df.groupby("CUSTOMER_RISK_SEGMENT")[["CUST_ID"]].nunique().reset_index()
    
    st.bar_chart(data = summary_df, x="CUSTOMER_RISK_SEGMENT", y = "CUST_ID" ,)
    