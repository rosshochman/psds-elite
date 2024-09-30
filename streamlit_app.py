import streamlit as st
import requests
from requests_oauthlib import OAuth2Session
from time import sleep
from urllib.parse import urlencode
import json

from navigation import make_sidebar

make_sidebar()

# Discord OAuth2 Credentials from Streamlit secrets
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
REDIRECT_URI = st.secrets["REDIRECT_URI"]
TARGET_GUILD_ID = st.secrets["TARGET_GUILD_ID"]  # The Guild ID of the server to check membership for

# OAuth2 URLs
AUTHORIZATION_BASE_URL = 'https://discord.com/api/oauth2/authorize'
TOKEN_URL = 'https://discord.com/api/oauth2/token'
USER_URL = 'https://discord.com/api/users/@me'
USER_GUILDS_URL = 'https://discord.com/api/users/@me/guilds'

# Initialize OAuth session
oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=["identify", "guilds"])

# Ensure session state for authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_with_discord():
    # Generate Discord login URL
    authorization_url, _ = oauth.authorization_url(AUTHORIZATION_BASE_URL)
    st.write(f"[Log in with Discord]({authorization_url})")

def fetch_discord_user_info(redirect_url):
    try:
        # Fetch the access token using the authorization response URL
        token = oauth.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=redirect_url)
        
        # Fetch basic user information
        user_info = requests.get(USER_URL, headers={'Authorization': f"Bearer {token['access_token']}"}).json()
        
        # Fetch user's guild memberships
        user_guilds = requests.get(USER_GUILDS_URL, headers={'Authorization': f"Bearer {token['access_token']}"}).json()
        
        return user_info, user_guilds
    
    except Exception as e:
        st.error(f"Error fetching token or user info: {str(e)}")
        return None, None

def check_guild_membership(user_guilds):
    # Check if the user is part of the target guild
    for guild in user_guilds:
        if guild['id'] == TARGET_GUILD_ID:
            return True
    return False

def authenticate_user():
    query_params = st.experimental_get_query_params()

    # Log the query parameters for debugging
    st.write("Query parameters received:", query_params)  # Debugging

    # Check if Discord has redirected with an authorization code
    if "code" in query_params:
        auth_code = query_params['code'][0]  # Extract the authorization code

        # Log the authorization code for debugging
        st.write(f"Authorization code received: {auth_code}")  # Debugging

        # Manually construct the full redirect URL
        full_redirect_url = REDIRECT_URI + "?" + urlencode(query_params)

        # Fetch user info and guild memberships
        user_info, user_guilds = fetch_discord_user_info(full_redirect_url)

        if user_info and user_guilds:
            # Check if the user is a member of the target guild
            if check_guild_membership(user_guilds):
                st.session_state.logged_in = True
                st.session_state.user_info = user_info
                st.success(f"Logged in as {user_info['username']}, and you're a member of the required guild!")
                sleep(0.5)
                st.switch_page("pages/page1.py")  # Redirect to another page after successful login
            else:
                st.error("You must be a member of the required Discord guild to access this app.")
    else:
        st.write("No authorization code found in URL.")

# Main App Layout
st.title("Welcome to Diamond Corp")

if st.session_state.logged_in:
    st.success(f"Already logged in as {st.session_state.user_info['username']}")
    st.switch_page("pages/page1.py")
else:
    authenticate_user()  # Check if the user has logged in
    st.write("Please log in to continue.")
    login_with_discord()
