from navigation import make_sidebar
import streamlit as st
st.set_page_config(layout="wide")
make_sidebar()
if st.session_state.get('logged_in', False):
    st.write(
        """
    # 🕵️ EVEN MORE SECRET
    
    This is a secret page that only logged-in users can see.
    
    Super duper secret.
    
    Shh....
    
    """
    )
if not st.session_state.get('logged_in', False):
    st.write("Forbidden")
