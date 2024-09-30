import streamlit as st
import requests
from requests_oauthlib import OAuth2Session
from time import sleep
from navigation import make_sidebar

make_sidebar()

# Discord OAuth2 Credentials
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
REDIRECT_URI = st.secrets["REDIRECT_URI"]
AUTHORIZATION_BASE_URL = 'https://discord.com/api/oauth2/authorize'
#AUTHORIZATION_BASE_URL = st.secrets["base_url"]
TOKEN_URL = 'https://discord.com/api/oauth2/token'
USER_URL = 'https://discord.com/api/users/@me'

# Initialize OAuth session
oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=["identify"])

# Ensure session state for authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_with_discord():
    # Generate Discord login URL
    authorization_url, _ = oauth.authorization_url(AUTHORIZATION_BASE_URL)

    # Redirect user to Discord for login
    st.write(f"[Log in with Discord]({authorization_url})")

def fetch_discord_user_info():
    token = oauth.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=st.experimental_get_query_params().get('url'))
    user_info = requests.get(USER_URL, headers={'Authorization': f"Bearer {token['access_token']}"}).json()
    return user_info

def authenticate_user():
    if "code" in st.experimental_get_query_params():
        user_info = fetch_discord_user_info()
        st.session_state.logged_in = True
        st.session_state.user_info = user_info
        st.success(f"Logged in as {user_info['username']}")
        sleep(0.5)
        st.switch_page("pages/page1.py")

# Main App Layout
st.title("Welcome to PSDS Elite")

if st.session_state.logged_in:
    st.success(f"Already logged in as {st.session_state.user_info['username']}")
    st.switch_page("pages/page1.py")
else:
    authenticate_user()  # Check if the user has logged in
    st.write("Please log in to continue.")
    login_with_discord()
