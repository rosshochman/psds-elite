from navigation import make_sidebar
import streamlit as st
from st_files_connection import FilesConnection

st.set_page_config(layout="wide")

conn = st.connection('gcs', type=FilesConnection)
df = conn.read("psds_streamlit/13G_13D_data.csv", input_format="csv", ttl=3600)



make_sidebar()
if st.session_state.get('logged_in', False):
    df1 = st.empty()
    df1.dataframe(df,use_container_width=True, hide_index=True)
if not st.session_state.get('logged_in', False):
    st.write("Forbidden")