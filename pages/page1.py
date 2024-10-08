from navigation import make_sidebar
import streamlit as st
from st_files_connection import FilesConnection

st.set_page_config(layout="wide")

conn = st.connection('gcs', type=FilesConnection)
df = conn.read("psds_streamlit/uploaded-data_test.csv", input_format="csv", ttl=3600)



make_sidebar()
if st.session_state.get('logged_in', False):
    st.markdown("Data below is for all small cap tickers. Please use the MultiSelect tools to filter for your search criteria.")
    col1, col2, col3= st.columns(3)
    if 'Ticker' in df.columns:
        df['Ticker'] = df['Ticker'].astype(str)
        unique_tickers = sorted(set(df['ticker']))
        with col1:
            selected_tickers = st.multiselect('Select Tickers:', options=unique_tickers)
        if selected_tickers:
            df = df[df['Ticker'].isin(selected_tickers)]
    if 'Sector' in df.columns:
        df['Sector'] = df['Sector'].astype(str)
        unique_sector = sorted(set(df['Sector']))
        with col2:
            selected_sector = st.multiselect('Select Sector:', options=unique_sector)
        if selected_sector:
            df = df[df['Sector'].isin(selected_sector)]
    if 'Industry' in df.columns:
        df['Industry'] = df['Industry'].astype(str)
        unique_industry = sorted(set(df['Industry']))
        with col3:
            selected_indsutry = st.multiselect('Select Industry:', options=unique_industry)
        if selected_indsutry:
            df = df[df['Industry'].isin(selected_indsutry)]
    df1 = st.empty()
    df1.dataframe(df, column_config={"Website": st.column_config.LinkColumn("Website"),
                                     "Description":st.column_config.Column(width="medium"),
                                     "Name":st.column_config.Column(width="medium"),
                                    "Sector":st.column_config.Column(width="medium"),
                                    "Industry":st.column_config.Column(width="medium")}, use_container_width=True, hide_index=True, height=1000)
if not st.session_state.get('logged_in', False):
    st.write("Forbidden")
