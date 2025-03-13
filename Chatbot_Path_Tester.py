# main file to be run by streamlit.
# Set up and run this Streamlit App

# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from helper_functions.utility import check_password
from logics.path_tester import vectorstore_path_tester
import io
import email

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Streamlit Path Tester"
)
# endregion <--------- Streamlit App Configuration --------->

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

## WHAT IS SHOWN ON THE APP STARTS FROM HERE!!!!

if 'page' not in st.session_state:
    st.session_state.page = 'input'

if 'response' not in st.session_state:
    st.session_state.response = None

if 'vectorstore_name' not in st.session_state:
    st.session_state.vectorstore_name = None

if st.session_state.page == 'input':
    st.title("Streamlit Path Tester")

    def generate_response(content):
        st.session_state.vectorstore_name = content
        with st.spinner('Checking...'):
            st.session_state.response = vectorstore_path_tester(st.session_state.vectorstore_name)
        st.session_state.page = 'output'
        st.rerun()

    vectorstore_name = st.text_input("Please enter the name of the vector store:")
    if st.button('Submit', type = 'primary'):
        if vectorstore_name:
            generate_response(vectorstore_name)
        else:
            st.warning("Please provide an input before submitting")

elif st.session_state.page == 'output':
    st.title('Result')
    st.write(st.session_state.response)

    if st.button('Back to Input'):
        st.session_state.page = 'input'
        st.session_state.response = None
        st.session_state.vectorstore_name = None
        st.rerun()



        


