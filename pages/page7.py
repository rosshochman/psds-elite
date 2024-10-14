from navigation import make_sidebar
import streamlit as st
st.set_page_config(layout="wide")
make_sidebar()
if st.session_state.get('logged_in', False):
    st.write(
        """
Ticker Lookup Coming Soon
    
    """
    )
if not st.session_state.get('logged_in', False):
    st.write("Forbidden")#ticker look up
#single select box to select ticker - then populate data frames and charts after selected
