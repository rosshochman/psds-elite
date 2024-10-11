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
    if 'float_min' not in st.session_state:
        st.session_state['float_min'] = df['Float'].min()
    if 'float_max' not in st.session_state:
        st.session_state['float_max'] = df['Float'].max()
    if 'marketcap_min' not in st.session_state:
        marketcap_min = df['MarketCap'].min()
        st.session_state['marketcap_min'] = int(marketcap_min)
    if 'marketcap_max' not in st.session_state:
        marketcap_max = df['MarketCap'].max()
        st.session_state['marketcap_max'] = int(marketcap_max)


    filtered_df = df.copy()

    if st.session_state['selected_tickers']:
        filtered_df = filtered_df[filtered_df['Ticker'].isin(st.session_state['selected_tickers'])]
    if st.session_state['selected_sector']:
        filtered_df = filtered_df[filtered_df['Sector'].isin(st.session_state['selected_sector'])]
    if st.session_state['selected_ind']:
        filtered_df = filtered_df[filtered_df['Industry'].isin(st.session_state['selected_ind'])]
    if st.session_state['float_min'] is not None and st.session_state['float_max'] is not None:    
        filtered_df = filtered_df[(filtered_df['Float'] >= st.session_state['float_min']) & 
                                  (filtered_df['Float'] <= st.session_state['float_max'])]
    if st.session_state['marketcap_min'] is not None and st.session_state['marketcap_max'] is not None:    
        filtered_df = filtered_df[(filtered_df['MarketCap'] >= st.session_state['marketcap_min']) & 
                                  (filtered_df['MarketCap'] <= st.session_state['marketcap_max'])]

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
    if 'Float' in df.columns:
        with col4:
            float_min = st.number_input('Minimum Float', value=int(st.session_state['float_min']), min_value=0)
            float_max = st.number_input('Maximum Float', value=int(st.session_state['float_max']), min_value=float_min)

            # Update session state and rerun if the values change
            if float_min != st.session_state['float_min'] or float_max != st.session_state['float_max']:
                st.session_state['float_min'] = float_min
                st.session_state['float_max'] = float_max
                st.rerun()

    if 'MarketCap' in df.columns:
        with col5:
            marketcap_min = st.number_input('Minimum MarketCap', value=int(st.session_state['marketcap_min']), min_value=0)
            marketcap_max = st.number_input('Maximum MarketCap', value=int(st.session_state['marketcap_max']), min_value=marketcap_min)

            # Update session state and rerun if the values change
            if marketcap_min != st.session_state['marketcap_min'] or marketcap_max != st.session_state['marketcap_max']:
                st.session_state['marketcap_min'] = marketcap_min
                st.session_state['marketcap_max'] = marketcap_max
                st.rerun()

    df1 = st.empty()
    df1.dataframe(filtered_df, column_config={"Website": st.column_config.LinkColumn("Website"),
                                     "Description":st.column_config.Column(width="medium"),
                                     "Name":st.column_config.Column(width="medium"),
                                    "Sector":st.column_config.Column(width="medium"),
                                    "Industry":st.column_config.Column(width="medium")}, use_container_width=True, hide_index=True, height=750)
if not st.session_state.get('logged_in', False):
    st.write("Forbidden")
