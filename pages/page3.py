from navigation import make_sidebar
import streamlit as st
from st_files_connection import FilesConnection
import re
import pandas as pd

st.set_page_config(layout="wide")

conn = st.connection('gcs', type=FilesConnection)
df = conn.read("psds_streamlit/13G_13D_data.csv", input_format="csv", ttl=3600)

#owners_split = df['Owners'].str.split('|', expand=True)
#owners_split.columns = [f'Owners {i+1}' for i in range(owners_split.shape[1])]
#df = pd.concat([df, owners_split], axis=1)


make_sidebar()
if st.session_state.get('logged_in', False):
    st.markdown("Data below is for all 13D/G filings for small cap tickers. Please use the MultiSelect tools to filter for your search criteria.")
    
    col1, col2, col3 = st.columns(3)
    
    # Initialize session state for selected options if not already set
    if 'selected_tickers' not in st.session_state:
        st.session_state['selected_tickers'] = []
        
    if 'selected_form' not in st.session_state:
        st.session_state['selected_form'] = []
        
    if 'selected_owners' not in st.session_state:
        st.session_state['selected_owners'] = []

    # Filtering for ticker multiselect
    if 'ticker' in df.columns:
        df['ticker'] = df['ticker'].astype(str)
        unique_tickers = sorted(set(df['ticker']))
        
        # Display multiselect for tickers
        with col1:
            st.session_state['selected_tickers'] = st.multiselect(
                'Select Tickers:',
                options=unique_tickers,
                default=st.session_state['selected_tickers']
            )
        
        # Filter the DataFrame based on ticker selection
        if st.session_state['selected_tickers']:
            df = df[df['ticker'].isin(st.session_state['selected_tickers'])]
    
    # Filtering for formType multiselect based on the filtered DataFrame (after ticker filtering)
    if 'formType' in df.columns:
        df['formType'] = df['formType'].astype(str)
        unique_form = sorted(set(df['formType']))  # Get formType options based on current filtered DataFrame
        
        with col2:
            st.session_state['selected_form'] = st.multiselect(
                'Select Form Type:',
                options=unique_form,  # Dynamic options based on filtered DataFrame
                default=st.session_state['selected_form']
            )
        
        # Further filter the DataFrame based on formType selection
        if st.session_state['selected_form']:
            df = df[df['formType'].isin(st.session_state['selected_form'])]
    
    # Filtering for Owners multiselect based on the filtered DataFrame (after ticker and formType filtering)
    if 'Owners' in df.columns:
        df['Owners'] = df['Owners'].astype(str)
        # Split Owners into individual components based on the current filtered DataFrame
        unique_owners = sorted(set(owner.strip() for owners_list in df['Owners'].str.split('|') for owner in owners_list if owner.strip()))
        
        with col3:
            st.session_state['selected_owners'] = st.multiselect(
                'Select Owners:',
                options=unique_owners,  # Dynamic options based on filtered DataFrame
                default=st.session_state['selected_owners']
            )
        
        # Further filter the DataFrame based on Owners selection
        if st.session_state['selected_owners']:
            df = df[df['Owners'].apply(lambda x: any(term.lower() in x.lower() for term in st.session_state['selected_owners']))]

    # Display the filtered DataFrame
    df1 = st.empty()
    df1.dataframe(df, use_container_width=True, hide_index=True, height=750)

else:
    st.write("Forbidden")
