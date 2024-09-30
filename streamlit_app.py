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

# Step 1: Display login button if not authenticated
if 'access_token' not in st.session_state:
    st.write("Click the button to log in with Discord")
    if st.button("Login with Discord"):
        # Redirect user to Discord's OAuth2 page
        auth_url = generate_discord_login_url()
        st.write(f"[Click here to authenticate with Discord]({auth_url})")

# Step 2: Handle the OAuth2 callback and check guild membership
elif 'access_token' in st.session_state:
    st.write("Checking your Discord guild memberships...")
    token = st.session_state['access_token']
    guilds = fetch_user_guilds(token)

    if is_user_in_guild(guilds):
        st.write("You are in the guild! Access granted.")
        # Display your Streamlit content here
    else:
        st.write("You are not in the required guild. Access denied.")

# Step 3: Capture OAuth2 callback
# Parse the URL query parameters manually
parsed_url = urlparse(st.experimental_get_url())
query_params = parse_qs(parsed_url.query)

if 'code' in query_params:
    code = query_params['code'][0]
    token_data = exchange_code_for_token(code)
    
    if 'access_token' in token_data:
        # Store access token in session state
        st.session_state['access_token'] = token_data['access_token']
        # Reload the app to move to authenticated state
        st.experimental_rerun()
