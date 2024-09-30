from navigation import make_sidebar
import streamlit as st

make_sidebar()
if st.session_state.get('logged_in', False):
    st.write(
        """
    # 🔓 Secret Company Stuff
    
    This is a secret page that only logged-in users can see.
    
    Don't tell anyone.
    
    For real.
    
    """
    )
if not st.session_state.get('logged_in', False):
    st.write("Forbidden")
