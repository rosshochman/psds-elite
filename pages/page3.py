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
    col1, col2, col3= st.columns(3)
    if 'Ticker' in df.columns:
        df['Ticker'] = df['Ticker'].astype(str)
        unique_tickers = sorted(set(df['Ticker']))
        with col1:
            selected_tickers = st.multiselect('Select Tickers:', options=unique_tickers)
        if selected_tickers:
            df = df[df['Ticker'].isin(selected_tickers)]
    if 'Form Type' in df.columns:
        df['Form Type'] = df['Form Type'].astype(str)
        unique_form = sorted(set(df['Form Type']))
        with col2:
            selected_form = st.multiselect('Select Form Type:', options=unique_form)
        if selected_form:
            df = df[df['Form Type'].isin(selected_form)]
    if 'Owners' in df.columns:
        df['Owners'] = df['Owners'].astype(str)
        unique_owners = sorted(set(owner.strip() for owners_list in df['Owners'].str.split('|') for owner in owners_list if owner.strip()))
        with col3:
            selected_owners = st.multiselect('Select Owners:', options=unique_owners)
        if selected_owners:
            df = df[df['Owners'].apply(lambda x: any(term.lower() in x.lower() for term in selected_owners))]
    df1 = st.empty()
    df1.dataframe(df, column_config={"HTML Link": st.column_config.LinkColumn("HTML Link", width="small),
                                     "Filing Link": st.column_config.LinkColumn("Filing Link", width="small")},
                                     use_container_width=True, hide_index=True, height=750)

if not st.session_state.get('logged_in', False):
    st.write("Forbidden")
