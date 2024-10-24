from navigation import make_sidebar
import streamlit as st
from st_files_connection import FilesConnection
import pandas as pd

st.set_page_config(layout="wide")


conn = st.connection('gcs', type=FilesConnection)
df_keyword = conn.read("psds_streamlit/full_text_final.csv", input_format="csv", ttl=3600)



make_sidebar()
if st.session_state.get('logged_in', False):
    st.write("""Keyword Tracker Coming Soon""")
    df1 = st.empty()
    df1.dataframe(df_keyword, use_container_width=True, hide_index=True, height=750)
if not st.session_state.get('logged_in', False):
    st.write("Forbidden")
