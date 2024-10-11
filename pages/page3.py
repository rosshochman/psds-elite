from navigation import make_sidebar
import streamlit as st
from st_files_connection import FilesConnection
import re
import pandas as pd

st.set_page_config(layout="wide")

conn = st.connection('gcs', type=FilesConnection)
df = conn.read("psds_streamlit/13G_13D_data.csv", input_format="csv", ttl=10)

#owners_split = df['Owners'].str.split('|', expand=True)
#owners_split.columns = [f'Owners {i+1}' for i in range(owners_split.shape[1])]
#df = pd.concat([df, owners_split], axis=1)


make_sidebar()

if st.session_state.get('logged_in', False):
    st.markdown("Data below is for all 13D/G filings for small cap tickers. Please use the MultiSelect tools to filter for your search criteria.")
    if 'selected_tickers' not in st.session_state:
        st.session_state['selected_tickers'] = []
    if 'selected_form' not in st.session_state:
        st.session_state['selected_form'] = []
    if 'selected_owners' not in st.session_state:
        st.session_state['selected_owners'] = []

    # Use the filtered DataFrame to update the multiselect options dynamically
    filtered_df = df.copy()

    # Apply filters based on session state
    if st.session_state['selected_tickers']:
        filtered_df = filtered_df[filtered_df['Ticker'].isin(st.session_state['selected_tickers'])]
    if st.session_state['selected_form']:
        filtered_df = filtered_df[filtered_df['Form Type'].isin(st.session_state['selected_form'])]
    if st.session_state['selected_owners']:
        filtered_df = filtered_df[filtered_df['All Owners'].apply(lambda x: any(term.lower() in x.lower() for term in st.session_state['selected_owners']))]
    
    # Get unique options based on the filtered DataFrame
    unique_tickers = sorted(set(filtered_df['Ticker']))
    unique_form = sorted(set(filtered_df['Form Type']))
    unique_owners = sorted(set(owner.strip() for owners_list in filtered_df['All Owners'].str.split('|') for owner in owners_list if owner.strip()))
    
    col1, col2, col3 = st.columns(3)
    
    # Ticker multiselect
    with col1:
        selected_tickers = st.multiselect('Select Tickers:', options=unique_tickers, default=st.session_state['selected_tickers'])
        if selected_tickers != st.session_state['selected_tickers']:
            st.session_state['selected_tickers'] = selected_tickers
            st.rerun()
    
    # Form Type multiselect
    with col2:
        selected_form = st.multiselect('Select Form Type:', options=unique_form, default=st.session_state['selected_form'])
        if selected_form != st.session_state['selected_form']:
            st.session_state['selected_form'] = selected_form
            st.rerun()
    
    # Owners multiselect
    with col3:
        selected_owners = st.multiselect('Select Owners:', options=unique_owners, default=st.session_state['selected_owners'])
        if selected_owners != st.session_state['selected_owners']:
            st.session_state['selected_owners'] = selected_owners
            st.rerun()
    
    # Display the filtered DataFrame
    df1 = st.empty()
    df1.dataframe(filtered_df, column_config={"Folder Link": st.column_config.LinkColumn("Folder Link", width="small"),
                                              "Place": st.column_config.Column(width="medium"),
                                              "Owners": st.column_config.Column(width="medium"),
                                              "Filing Link": st.column_config.LinkColumn("Filing Link", width="small")},
                                              use_container_width=True, hide_index=True, height=750)

if not st.session_state.get('logged_in', False):
    st.write("Forbidden")
