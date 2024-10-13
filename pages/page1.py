from navigation import make_sidebar
import streamlit as st
from st_files_connection import FilesConnection
import pandas as pd

st.set_page_config(layout="wide")
conn = st.connection('gcs', type=FilesConnection)
df = conn.read("psds_streamlit/uploaded-data_test.csv", input_format="csv", ttl=5)
#df['MarketCap'] = df['MarketCap'].fillna(0)
#df['Float'] = df['MarketCap'].fillna(0)
#df['Float'] = pd.to_numeric(df['Float'], errors='coerce') 
#df['MarketCap'] = pd.to_numeric(df['MarketCap'], errors='coerce')
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
    if 'selected_inc' not in st.session_state:
        st.session_state['selected_inc'] = []
    if 'selected_country' not in st.session_state:
        st.session_state['selected_country'] = []

    filtered_df = df.copy()

    if st.session_state['selected_tickers']:
        filtered_df = filtered_df[filtered_df['Ticker'].isin(st.session_state['selected_tickers'])]
    if st.session_state['selected_sector']:
        filtered_df = filtered_df[filtered_df['Sector'].isin(st.session_state['selected_sector'])]
    if st.session_state['selected_ind']:
        filtered_df = filtered_df[filtered_df['Industry'].isin(st.session_state['selected_ind'])]
    if st.session_state['selected_inc']:
        filtered_df = filtered_df[filtered_df['Country Incorporation'].isin(st.session_state['selected_inc'])]
    if st.session_state['selected_country']:
        filtered_df = filtered_df[filtered_df['Country'].isin(st.session_state['selected_country'])]

    unique_tickers = sorted(set(filtered_df['Ticker'].dropna().astype(str)))
    unique_sector = sorted(set(filtered_df['Sector'].dropna().astype(str)))
    unique_ind = sorted(set(filtered_df['Industry'].dropna().astype(str)))
    unique_inc = sorted(set(filtered_df['Country Incorporation'].dropna().astype(str)))
    unique_country = sorted(set(filtered_df['Country'].dropna().astype(str)))

    valid_selected_tickers = [ticker for ticker in st.session_state['selected_tickers'] if ticker in unique_tickers]
    valid_selected_sector = [sector for sector in st.session_state['selected_sector'] if sector in unique_sector]
    valid_selected_ind = [ind for ind in st.session_state['selected_ind'] if ind in unique_ind]
    valid_selected_inc = [inc for inc in st.session_state['selected_inc'] if inc in unique_inc]
    valid_selected_country = [country for country in st.session_state['selected_country'] if country in unique_country]
    
    st.markdown("Data below is for all small cap tickers. Please use the MultiSelect tools to filter for your search criteria.")
    col1, col2, col3, col4, col5 = st.columns(5)
    if 'Ticker' in df.columns:
        with col1:
            selected_tickers = st.multiselect('Select Tickers:', options=unique_tickers, default=valid_selected_tickers)
            col1_1, col1_2= st.columns(2)
            with col1_1:
                if st.button('Apply Ticker', use_container_width=True):
                    st.session_state['selected_tickers'] = selected_tickers
                    st.rerun()
            with col1_2:
                if st.button('Reset Ticker', type='primary', use_container_width=True):
                    st.session_state['selected_tickers'] = []
                    st.rerun()
    if 'Sector' in df.columns:
        with col2:
            selected_sector = st.multiselect('Select Sector:', options=unique_sector, default=valid_selected_sector)
            col2_1, col2_2= st.columns(2)
            with col2_1:
                if st.button('Apply Sector', use_container_width=True):
                    st.session_state['selected_sector'] = selected_sector
                    st.rerun()
            with col2_2:
                if st.button('Reset Sector', type='primary', use_container_width=True):
                    st.session_state['selected_sector'] = []
                    st.rerun()
    if 'Industry' in df.columns:
        with col3:
            selected_ind = st.multiselect('Select Industry:', options=unique_ind, default=valid_selected_ind)
            col3_1, col3_2= st.columns(2)
            with col3_1:
                if st.button('Apply Industry', use_container_width=True):
                    st.session_state['selected_ind'] = selected_ind
                    st.rerun()
            with col3_2:
                if st.button('Reset Industry', type='primary', use_container_width=True):
                    st.session_state['selected_ind'] = []
                    st.rerun()
    if 'State Incorporation' in df.columns:
        with col4:
            selected_inc = st.multiselect('Select Country Incorporation:', options=unique_inc, default=valid_selected_inc)
            col4_1, col4_2= st.columns(2)
            with col4_1:
                if st.button('Apply CI', use_container_width=True):
                    st.session_state['selected_inc'] = selected_inc
                    st.rerun()
            with col4_2:
                if st.button('Reset CI', type='primary', use_container_width=True):
                    st.session_state['selected_inc'] = []
                    st.rerun()
    if 'State/Country' in df.columns:
        with col5:
            selected_country = st.multiselect('Select Country:', options=unique_country, default=valid_selected_country)
            col5_1, col5_2= st.columns(2)
            with col5_1:
                if st.button('Apply Country', use_container_width=True):
                    st.session_state['selected_country'] = selected_country
                    st.rerun()
            with col5_2:
                if st.button('Reset Country', type='primary', use_container_width=True):
                    st.session_state['selected_country'] = []
                    st.rerun()


    df1 = st.empty()
    df1.dataframe(filtered_df, column_config={"Website": st.column_config.LinkColumn("Website"),
                                     "Description":st.column_config.Column(width="medium"),
                                     "Name":st.column_config.Column(width="medium"),
                                    "Sector":st.column_config.Column(width="medium"),
                                    "Industry":st.column_config.Column(width="medium")}, use_container_width=True, hide_index=True, height=750)
if not st.session_state.get('logged_in', False):
    st.write("Forbidden")
