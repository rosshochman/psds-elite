import streamlit as st
import requests
from urllib.parse import urlencode, urlparse, parse_qs

# Discord OAuth2 credentials
client_id = st.secrets["CLIENT_ID"]
client_secret = st.secrets["CLIENT_SECRET"]
redirect_uri = st.secrets["REDIRECT_URI"]

# Discord guild ID to check
guild_id = st.secrets["TARGET_GUILD_ID"]


# Generate the Discord login URL
def generate_discord_login_url():
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'identify guilds',
    }
    return f"https://discord.com/api/oauth2/authorize?{urlencode(params)}"

# Function to exchange the authorization code for an access token
def exchange_code_for_token(code):
    url = 'https://discord.com/api/oauth2/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=data, headers=headers)
    return response.json()

# Fetch user's guilds with the access token
def fetch_user_guilds(token):
    url = 'https://discord.com/api/users/@me/guilds'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    return response.json()

# Check if the user is in the specific guild
def is_user_in_guild(guilds):
    return any(guild['id'] == guild_id for guild in guilds)

# Step 1: Capture OAuth2 callback code automatically when user is redirected
query_params = st.experimental_get_query_params()

if 'code' in query_params and 'access_token' not in st.session_state:
    # Automatically exchange the code for an access token
    code = query_params['code'][0]
    token_data = exchange_code_for_token(code)

    if 'access_token' in token_data:
        # Store access token in session state
        st.session_state['access_token'] = token_data['access_token']
        # Optionally clear the URL of the code parameter
        st.experimental_set_query_params()

# Step 2: If user is authenticated, check their guild membership
if 'access_token' in st.session_state:
    st.write("Checking your Discord guild memberships...")
    token = st.session_state['access_token']
    guilds = fetch_user_guilds(token)

    if is_user_in_guild(guilds):
        st.write("You are in the guild! Access granted.")
        # Display your Streamlit content here
    else:
        st.write("You are not in the required guild. Access denied.")
else:
    # Step 3: Display login button if not authenticated
    st.write("Click the button to log in with Discord")
    if st.button("Login with Discord"):
        # Redirect user to Discord's OAuth2 page
        auth_url = generate_discord_login_url()
        st.write(f"[Click here to authenticate with Discord]({auth_url})")
