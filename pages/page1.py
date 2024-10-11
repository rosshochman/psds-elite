from navigation import make_sidebar
import streamlit as st
from st_files_connection import FilesConnection

st.set_page_config(layout="wide")

conn = st.connection('gcs', type=FilesConnection)
df = conn.read("psds_streamlit/uploaded-data_test.csv", input_format="csv", ttl=3600)

#if 'filtered_df' not in st.session_state:
    #st.session_state['filtered_df'] = df.copy()

make_sidebar()
if st.session_state.get('logged_in', False):
    if 'selected_tickers' not in st.session_state:
        st.session_state['selected_tickers'] = []
    if 'selected_sector' not in st.session_state:
        st.session_state['selected_sector'] = []
    if 'selected_industry' not in st.session_state:
        st.session_state['selected_industry'] = []

    st.markdown("Data below is for all small cap tickers. Please use the MultiSelect tools to filter for your search criteria.")
    
    # Create 4 columns for the multiselect and text input
    col1, col2, col3, col4 = st.columns(4)
    
    # Ticker multiselect
    if 'Ticker' in df.columns:
        df['Ticker'] = df['Ticker'].astype(str)
        unique_tickers = sorted(set(df['Ticker']))
        with col1:
            selected_tickers = st.multiselect('Select Tickers:', options=unique_tickers, default=st.session_state['selected_tickers'])
            if selected_tickers != st.session_state['selected_tickers']:
                st.session_state['selected_tickers'] = selected_tickers
                st.rerun()
    
    # Sector multiselect
    if 'Sector' in df.columns:
        df['Sector'] = df['Sector'].astype(str)
        unique_sector = sorted(set(df['Sector']))
        with col2:
            selected_sector = st.multiselect('Select Sector:', options=unique_sector, default=st.session_state['selected_sector'])
            if selected_sector != st.session_state['selected_sector']:
                st.session_state['selected_sector'] = selected_sector
                st.rerun()
    
    # Industry multiselect
    if 'Industry' in df.columns:
        df['Industry'] = df['Industry'].astype(str)
        unique_industry = sorted(set(df['Industry']))
        with col3:
            selected_industry = st.multiselect('Select Industry:', options=unique_industry, default=st.session_state['selected_industry'])
            if selected_industry != st.session_state['selected_industry']:
                st.session_state['selected_industry'] = selected_industry
                st.rerun()

    # Apply filters from session state
    if st.session_state['selected_tickers']:
        df = df[df['Ticker'].isin(st.session_state['selected_tickers'])]
    if st.session_state['selected_sector']:
        df = df[df['Sector'].isin(st.session_state['selected_sector'])]
    if st.session_state['selected_industry']:
        df = df[df['Industry'].isin(st.session_state['selected_industry'])]
    
    # Display filtered DataFrame

    df1 = st.empty()
    df1.dataframe(df, column_config={"Website": st.column_config.LinkColumn("Website"),
                                     "Description":st.column_config.Column(width="medium"),
                                     "Name":st.column_config.Column(width="medium"),
                                    "Sector":st.column_config.Column(width="medium"),
                                    "Industry":st.column_config.Column(width="medium")}, use_container_width=True, hide_index=True, height=750)


if not st.session_state.get('logged_in', False):
    st.write("Forbidden")
