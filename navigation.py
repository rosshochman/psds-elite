import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.title("PSDS Elite")
        st.write("")
        st.write("")

        if st.session_state.get('logged_in', False):
            st.page_link("pages/page1.py", label="Small Cap Screener")
            st.page_link("pages/page2.py", label="Catalyst Tracker")
            st.page_link("pages/page3.py", label="13G/13D Tracker")
            st.page_link("pages/page4.py", label="IPO Tracker")
            st.page_link("pages/page5.py", label="Lockup Expiration Tracker")
            st.page_link("pages/page6.py", label="Keyword Tracker")
            st.page_link("pages/page7.py", label="Ticker Lookup")
            st.page_link("pages/page8.py", label="SEC Litigation & News Full Text Search")
    
            st.write("")
            st.write("")
    
            if st.button("Log out"):
                logout()

        elif get_current_page_name() != "streamlit_app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.markdown('[Go to Main Page](https://psds-elite.streamlit.app/)')
            #st.switch_page("streamlit_app.py")


def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.markdown('[Go to Main Page](https://psds-elite.streamlit.app/)')
