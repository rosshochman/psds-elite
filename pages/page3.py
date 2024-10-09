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

    # Step 1: Dynamically calculate the available options for each multiselect
    df_unfiltered = df.copy()

    # Available Owners based on the current DataFrame ignoring the Owners filter
    df_owners_filtered = df_unfiltered.copy()
    if st.session_state['selected_tickers']:
        df_owners_filtered = df_owners_filtered[df_owners_filtered['ticker'].isin(st.session_state['selected_tickers'])]
    if st.session_state['selected_form']:
        df_owners_filtered = df_owners_filtered[df_owners_filtered['formType'].isin(st.session_state['selected_form'])]
    unique_owners = sorted(set(
        owner.strip() for owners_list in df_owners_filtered['Owners'].fillna('').str.split('|') for owner in owners_list if owner.strip()
    ))

    # Available Tickers based on the current DataFrame ignoring the Ticker filter
    df_tickers_filtered = df_unfiltered.copy()
    if st.session_state['selected_owners']:
        df_tickers_filtered = df_tickers_filtered[df_tickers_filtered['Owners'].apply(lambda x: any(term.lower() in x.lower() for term in st.session_state['selected_owners']) if pd.notnull(x) else False)]
    if st.session_state['selected_form']:
        df_tickers_filtered = df_tickers_filtered[df_tickers_filtered['formType'].isin(st.session_state['selected_form'])]
    unique_tickers = sorted(set(df_tickers_filtered['ticker']))

    # Available Form Types based on the current DataFrame ignoring the Form Type filter
    df_form_filtered = df_unfiltered.copy()
    if st.session_state['selected_owners']:
        df_form_filtered = df_form_filtered[df_form_filtered['Owners'].apply(lambda x: any(term.lower() in x.lower() for term in st.session_state['selected_owners']) if pd.notnull(x) else False)]
    if st.session_state['selected_tickers']:
        df_form_filtered = df_form_filtered[df_form_filtered['ticker'].isin(st.session_state['selected_tickers'])]
    unique_form = sorted(set(df_form_filtered['formType']))

    # Step 2: Render the multiselects using the updated options
    with col3:
        selected_owners = st.multiselect(
            'Select Owners:',
            options=unique_owners,
            default=st.session_state['selected_owners']
        )
        st.session_state['selected_owners'] = selected_owners

    with col1:
        selected_tickers = st.multiselect(
            'Select Tickers:',
            options=unique_tickers,
            default=st.session_state['selected_tickers']
        )
        st.session_state['selected_tickers'] = selected_tickers

    with col2:
        selected_form = st.multiselect(
            'Select Form Type:',
            options=unique_form,
            default=st.session_state['selected_form']
        )
        st.session_state['selected_form'] = selected_form

    # Step 3: Apply the filters to the DataFrame based on the final selections
    df_final = df.copy()

    if st.session_state['selected_owners']:
        df_final = df_final[df_final['Owners'].apply(lambda x: any(term.lower() in x.lower() for term in st.session_state['selected_owners']) if pd.notnull(x) else False)]
    
    if st.session_state['selected_tickers']:
        df_final = df_final[df_final['ticker'].isin(st.session_state['selected_tickers'])]

    if st.session_state['selected_form']:
        df_final = df_final[df_final['formType'].isin(st.session_state['selected_form'])]

    # Display the final filtered DataFrame
    df1 = st.empty()
    df1.dataframe(df_final, use_container_width=True, hide_index=True, height=750)

else:
    st.write("Forbidden")
