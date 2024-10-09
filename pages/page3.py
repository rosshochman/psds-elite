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

    # Create a copy of the DataFrame for filtering
    df_filtered = df.copy()

    # Apply filtering based on the current selections in all multiselects, regardless of order

    # Apply Owners filter
    if st.session_state['selected_owners']:
        df_filtered = df_filtered[df_filtered['Owners'].apply(lambda x: any(term.lower() in x.lower() for term in st.session_state['selected_owners']))]

    # Apply Ticker filter
    if st.session_state['selected_tickers']:
        df_filtered = df_filtered[df_filtered['ticker'].isin(st.session_state['selected_tickers'])]

    # Apply Form Type filter
    if st.session_state['selected_form']:
        df_filtered = df_filtered[df_filtered['formType'].isin(st.session_state['selected_form'])]

    # Dynamically calculate the options for each multiselect based on the filtered DataFrame
    # Available options for Tickers, Form Types, and Owners based on the current state of the filtered DataFrame
    unique_tickers = sorted(set(df_filtered['ticker']))
    unique_form = sorted(set(df_filtered['formType']))
    unique_owners = sorted(set(
        owner.strip() for owners_list in df_filtered['Owners'].fillna('').str.split('|') for owner in owners_list if owner.strip()
    ))

    # Display multiselect for Owners
    with col3:
        st.session_state['selected_owners'] = st.multiselect(
            'Select Owners:',
            options=unique_owners,  # Dynamically updated based on filtered DataFrame
            default=st.session_state['selected_owners']
        )

    # Display multiselect for Tickers
    with col1:
        st.session_state['selected_tickers'] = st.multiselect(
            'Select Tickers:',
            options=unique_tickers,  # Dynamically updated based on filtered DataFrame
            default=st.session_state['selected_tickers']
        )

    # Display multiselect for Form Type
    with col2:
        st.session_state['selected_form'] = st.multiselect(
            'Select Form Type:',
            options=unique_form,  # Dynamically updated based on filtered DataFrame
            default=st.session_state['selected_form']
        )

    # Apply the filters again based on the new selections (this ensures everything updates correctly)
    df_final = df.copy()

    # Owners filter
    if st.session_state['selected_owners']:
        df_final = df_final[df_final['Owners'].apply(lambda x: any(term.lower() in x.lower() for term in st.session_state['selected_owners']))]

    # Ticker filter
    if st.session_state['selected_tickers']:
        df_final = df_final[df_final['ticker'].isin(st.session_state['selected_tickers'])]

    # Form Type filter
    if st.session_state['selected_form']:
        df_final = df_final[df_final['formType'].isin(st.session_state['selected_form'])]

    # Display the final filtered DataFrame
    df1 = st.empty()
    df1.dataframe(df_final, use_container_width=True, hide_index=True, height=750)

else:
    st.write("Forbidden")
