from navigation import make_sidebar
import streamlit as st
from st_files_connection import FilesConnection

st.set_page_config(layout="wide")

df1 = st.empty()

make_sidebar()
if st.session_state.get('logged_in', False):
    conn = st.connection('gcs', type=FilesConnection)
    df = conn.read("psds_streamlit/uploaded-data_test.csv", input_format="csv", ttl=600)
    df1.dataframe(df, hide_index=True)
if not st.session_state.get('logged_in', False):
    st.write("Forbidden")
