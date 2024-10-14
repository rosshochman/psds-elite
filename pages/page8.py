from navigation import make_sidebar
import streamlit as st
st.set_page_config(layout="wide")
make_sidebar()
if st.session_state.get('logged_in', False):
    st.write(
        """
SEC Litigation & News Full Text Search Coming Soon
    
    """
    )
if not st.session_state.get('logged_in', False):
    st.write("Forbidden")
