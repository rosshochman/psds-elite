from navigation import make_sidebar
import streamlit as st
from st_files_connection import FilesConnection
import pandas as pd

st.set_page_config(layout="wide")
conn = st.connection('gcs', type=FilesConnection)
df = conn.read("psds_streamlit/uploaded-data_test.csv", input_format="csv", ttl=3600)
# Check if "NA" is present in the 'Ticker' column before replacing it
df['Ticker'] = df['Ticker'].fillna('NA')
ticker_options = ['Select a Ticker'] + list(df['Ticker'].unique())


make_sidebar()
if st.session_state.get('logged_in', False):
    st.write("""Ticker Lookup Coming Soon""")
    selected_ticker = st.selectbox('Select Ticker:', ticker_options)
    if selected_ticker != 'Select a Ticker':
        st.write(f'You selected: {selected_ticker}')
    else:
        st.write('Please select a Ticker')
if not st.session_state.get('logged_in', False):
    st.write("Forbidden")#ticker look up
#single select box to select ticker - then populate data frames and charts after selected
