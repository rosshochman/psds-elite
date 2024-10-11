from navigation import make_sidebar
import streamlit as st
from st_files_connection import FilesConnection
import pandas as pd

st.set_page_config(layout="wide")

conn = st.connection('gcs', type=FilesConnection)
df = conn.read("psds_streamlit/uploaded-data_test.csv", input_format="csv", ttl=3600)
df['MarketCap'] = df['MarketCap'].fillna(0)
df['Float'] = pd.to_numeric(df['Float'], errors='coerce') 
df['MarketCap'] = pd.to_numeric(df['MarketCap'], errors='coerce')
#if 'filtered_df' not in st.session_state:
    #st.session_state['filtered_df'] = df.copy()

make_sidebar()
if st.session_state.get('logged_in', False):
    if 'selected_tickers' not in st.session_state:
        st.session_state['selected_tickers'] = []
    if 'selected_sector' not in st.session_state:
        st.session_state['selected_sector'] = []
    if 'selected_ind' not in st.session_state:
        st.session_state['selected_ind'] = []
    if 'float_range' not in st.session_state:
        st.session_state['float_range'] = (df['Float'].min(), df['Float'].max())
    if 'marketcap_range' not in st.session_state:
        marketcap_min = df['MarketCap'].min()
        marketcap_max = df['MarketCap'].max()
        if pd.isna(marketcap_min):
            marketcap_min = 0
        if pd.isna(marketcap_max):
            marketcap_max = 1 
        st.session_state['marketcap_range'] = (marketcap_min, marketcap_max)

    filtered_df = df.copy()

    if st.session_state['selected_tickers']:
        filtered_df = filtered_df[filtered_df['Ticker'].isin(st.session_state['selected_tickers'])]
    if st.session_state['selected_sector']:
        filtered_df = filtered_df[filtered_df['Sector'].isin(st.session_state['selected_sector'])]
    if st.session_state['selected_ind']:
        filtered_df = filtered_df[filtered_df['Industry'].isin(st.session_state['selected_ind'])]
    if st.session_state['float_range']:    
        filtered_df = filtered_df[(filtered_df['Float'] >= st.session_state['float_range'][0]) & (filtered_df['Float'] <= st.session_state['float_range'][1])]
    if st.session_state['marketcap_range']:    
        filtered_df = filtered_df[(filtered_df['MarketCap'] >= st.session_state['marketcap_range'][0]) & (filtered_df['MarketCap'] <= st.session_state['marketcap_range'][1])]

    unique_tickers = sorted(set(filtered_df['Ticker'].astype(str)))
    unique_sector = sorted(set(filtered_df['Sector'].astype(str)))
    unique_ind = sorted(set(filtered_df['Industry'].astype(str)))
    
    st.markdown("Data below is for all small cap tickers. Please use the MultiSelect tools to filter for your search criteria.")
    col1, col2, col3, col4, col5= st.columns(5)
    if 'Ticker' in df.columns:
        with col1:
            selected_tickers = st.multiselect('Select Tickers:', options=unique_tickers, default=st.session_state['selected_tickers'])
            if selected_tickers != st.session_state['selected_tickers']:
                st.session_state['selected_tickers'] = selected_tickers
                st.rerun()
    if 'Sector' in df.columns:
        with col2:
            selected_sector = st.multiselect('Select Sector:', options=unique_sector, default=st.session_state['selected_sector'])
            if selected_sector != st.session_state['selected_sector']:
                st.session_state['selected_sector'] = selected_sector
                st.rerun()
    if 'Industry' in df.columns:
        with col3:
            selected_ind = st.multiselect('Select Industry:', options=unique_ind, default=st.session_state['selected_ind'])
            if selected_ind != st.session_state['selected_ind']:
                st.session_state['selected_ind'] = selected_ind
                st.rerun()


    df1 = st.empty()
    df1.dataframe(filtered_df, column_config={"Website": st.column_config.LinkColumn("Website"),
                                     "Description":st.column_config.Column(width="medium"),
                                     "Name":st.column_config.Column(width="medium"),
                                    "Sector":st.column_config.Column(width="medium"),
                                    "Industry":st.column_config.Column(width="medium")}, use_container_width=True, hide_index=True, height=750)
if not st.session_state.get('logged_in', False):
    st.write("Forbidden")
