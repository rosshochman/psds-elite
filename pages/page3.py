from navigation import make_sidebar
import streamlit as st
from st_files_connection import FilesConnection

st.set_page_config(layout="wide")

conn = st.connection('gcs', type=FilesConnection)
df = conn.read("psds_streamlit/13G_13D_data.csv", input_format="csv", ttl=3600)



make_sidebar()
if st.session_state.get('logged_in', False):
    st.subheader("Filter by Ticker")
    if 'ticker' in df.columns:
        unique_tickers = sorted(set(df['ticker']))
        selected_tickers = st.multiselect('Select Tickers:', options=unique_tickers)
        if selected_tickers:
            df = df[df['ticker'].isin(selected_tickers)]
    #if 'owners1.name' in df.columns:
    #    unique_owners = sorted(set(df['owners1.name']))
    #    selected_owners = st.multiselect('Select Owners:', options=unique_owners)
    #    if selected_owners:
    #        df = df[df['owners1.name'].isin(selected_owners)]
    df1 = st.empty()
    df1.dataframe(df,use_container_width=True, hide_index=True)

if not st.session_state.get('logged_in', False):
    st.write("Forbidden")
