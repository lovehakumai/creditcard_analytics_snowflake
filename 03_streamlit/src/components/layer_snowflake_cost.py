import streamlit as st 
import pandas as pd 
from src.models.get_data_for_metrics_1 import get_data_for_metrics_1

def layer_snowflake_cost():
    # 1. データの取得（原本汚染を防ぐためcopyを推奨）
    df = get_data_for_metrics_1().copy()
    df['YEAR_MONTH'] = df['START_TIME'].dt.strftime('%Y-%m')
    
    # 2. サイドバーUIの設置
    col1, col2, col3 = st.columns(3)
    with col1:
        time_granularity = st.radio("Month or Date", ["MONTH", "DATE"])
        unique_months = sorted(df['YEAR_MONTH'].unique())
    with col2: 
        start_month = st.selectbox("START", unique_months, index=0)
    with col3: 
        end_month = st.selectbox("END", unique_months, index=len(unique_months)-1)

    # 3. 選択された「月範囲」でフィルタリング
    filtered_df = df[(df['YEAR_MONTH'] >= start_month) & (df['YEAR_MONTH'] <= end_month)].copy()

    # 4. 【修正】選択された粒度（MONTH / DATE）に応じた集計ロジック
    if time_granularity == 'MONTH':
        # 月ごとに集計（YEAR_MONTH カラムを使用）
        summary_df = filtered_df.groupby('YEAR_MONTH')['CREDITS_USED'].sum().reset_index()
        x_axis = 'YEAR_MONTH'
    else:
        # 日ごとに集計（START_TIME から日付部分を抽出。※カッコは不要）
        filtered_df["PLOT_DATE"] = filtered_df["START_TIME"].dt.date
        summary_df = filtered_df.groupby('PLOT_DATE')['CREDITS_USED'].sum().reset_index()
        x_axis = 'PLOT_DATE'

    # 5. 画面への描画
    total_filtered_credits = summary_df['CREDITS_USED'].sum()
    st.metric(label="Total Cost", value=f"{total_filtered_credits:,.2f} Credits")
    st.line_chart(data=summary_df, x=x_axis, y='CREDITS_USED')