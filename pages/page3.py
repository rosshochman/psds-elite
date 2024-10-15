from navigation import make_sidebar
import streamlit as st
from st_files_connection import FilesConnection
import re
import pandas as pd

st.set_page_config(layout="wide")
#test
conn = st.connection('gcs', type=FilesConnection)
df = conn.read("psds_streamlit/13G_13D_data.csv", input_format="csv", ttl=5)
df['All Owners'] = df['All Owners'].fillna('')

#owners_split = df['Owners'].str.split('|', expand=True)
#owners_split.columns = [f'Owners {i+1}' for i in range(owners_split.shape[1])]
#df = pd.concat([df, owners_split], axis=1)


make_sidebar()

if st.session_state.get('logged_in', False):
    st.markdown("Data below is for all 13D/G filings for small cap tickers. Please use the MultiSelect tools to filter for your search criteria.")
    if 'selected_tickers_2' not in st.session_state:
        st.session_state['selected_tickers_2'] = []
    if 'selected_form_2' not in st.session_state:
        st.session_state['selected_form_2'] = []
    if 'selected_owners_2' not in st.session_state:
        st.session_state['selected_owners_2'] = []
    if 'selected_filer_2' not in st.session_state:
        st.session_state['selected_filer_2'] = []
    if 'selected_country_2' not in st.session_state:
        st.session_state['selected_country_2'] = []

    # Use the filtered DataFrame to update the multiselect options dynamically
    filtered_df = df.copy()

    # Apply filters based on session state
    if st.session_state['selected_tickers_2']:
        filtered_df = filtered_df[filtered_df['Ticker'].isin(st.session_state['selected_tickers_2'])]
    if st.session_state['selected_form_2']:
        filtered_df = filtered_df[filtered_df['Form Type'].isin(st.session_state['selected_form_2'])]
    if st.session_state['selected_owners_2']:
        filtered_df = filtered_df[filtered_df['All Owners'].apply(lambda x: any(term.lower() in x.lower() for term in st.session_state['selected_owners_2']))]
    if st.session_state['selected_filer_2']:
        filtered_df = filtered_df[filtered_df['Filer Name'].isin(st.session_state['selected_filer_2'])]
    if st.session_state['selected_country_2']:
        filtered_df = filtered_df[filtered_df['Filer Country'].isin(st.session_state['selected_country_2'])]
    
    # Exclude NaN values using dropna() for Ticker and Form Type
    unique_tickers = sorted(set(filtered_df['Ticker'].dropna()))
    unique_form = sorted(set(filtered_df['Form Type'].dropna()))
    
    # For 'All Owners', ensure that NaN values are handled before splitting the strings
    unique_owners = sorted(set(owner.strip() 
        for owners_list in filtered_df['All Owners'].dropna().str.split('|') 
        for owner in owners_list if owner.strip()))
    
    unique_filer = sorted(set(filtered_df['Filer Name'].dropna()))
    unique_country = sorted(set(filtered_df['Filer Country'].dropna()))
    
    valid_selected_tickers = [ticker for ticker in st.session_state['selected_tickers_2'] if ticker in unique_tickers]
    valid_selected_form = [form for form in st.session_state['selected_form_2'] if form in unique_form]
    valid_selected_owners = [owners for owners in st.session_state['selected_owners_2'] if owners in unique_owners]
    valid_selected_filer = [filer for filer in st.session_state['selected_filer_2'] if filer in unique_filer]
    valid_selected_country = [country for country in st.session_state['selected_country_2'] if country in unique_country]

    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Ticker multiselect
    with col1:
        selected_tickers = st.multiselect('Select Ticker:', options=unique_tickers, default=valid_selected_tickers)
        col1_1, col1_2= st.columns(2)
        with col1_1:
            if st.button('Apply Ticker', use_container_width=True):
                st.session_state['selected_tickers_2'] = selected_tickers
                st.rerun()
        with col1_2:
            if st.button('Reset Ticker', type='primary', use_container_width=True):
                st.session_state['selected_tickers_2'] = []
                st.rerun()
    
    # Form Type multiselect
    with col2:
        selected_form = st.multiselect('Select Form Type:', options=unique_form, default=valid_selected_form)
        col1_1, col1_2= st.columns(2)
        with col1_1:
            if st.button('Apply Form', use_container_width=True):
                st.session_state['selected_form_2'] = selected_form
                st.rerun()
        with col1_2:
            if st.button('Reset Form', type='primary', use_container_width=True):
                st.session_state['selected_form_2'] = []
                st.rerun()    
    # Owners multiselect
    with col3:
        selected_owners = st.multiselect('Select Owner:', options=unique_owners, default=valid_selected_owners)
        col1_1, col1_2= st.columns(2)
        with col1_1:
            if st.button('Apply Owner', use_container_width=True):
                st.session_state['selected_owners_2'] = selected_owners
                st.rerun()
        with col1_2:
            if st.button('Reset Owner', type='primary', use_container_width=True):
                st.session_state['selected_owners_2'] = []
                st.rerun()   
    with col4:
        selected_filer = st.multiselect('Select Filer:', options=unique_filer, default=valid_selected_filer)
        col4_1, col4_2= st.columns(2)
        with col4_1:
            if st.button('Apply Filer', use_container_width=True):
                st.session_state['selected_filer_2'] = selected_filer
                st.rerun()
        with col4_2:
            if st.button('Reset Filer', type='primary', use_container_width=True):
                st.session_state['selected_filer_2'] = []
                st.rerun()   
    with col5:
        selected_country = st.multiselect('Select Country:', options=unique_country, default=valid_selected_country)
        col5_1, col5_2= st.columns(2)
        with col5_1:
            if st.button('Apply Country', use_container_width=True):
                st.session_state['selected_country_2'] = selected_country
                st.rerun()
        with col5_2:
            if st.button('Reset Country', type='primary', use_container_width=True):
                st.session_state['selected_country_2'] = []
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
