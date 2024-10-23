# main file to be run by streamlit.
# Set up and run this Streamlit App
import streamlit as st
from helper_functions.utility import text_import 
from helper_functions.utility import email_msg_import
from helper_functions.utility import check_password
from logics.water_quality_query_handler_matthew import process_user_message_wq
import io
import email

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

## WHAT IS SHOWN ON THE APP STARTS FROM HERE!!!!

if 'page' not in st.session_state:
    st.session_state.page = 'input'

if st.session_state.page == 'input':
    st.title("Water Quality Email Response Generator")

    with st.expander('Click to see disclaimer'):
        st.write('''
        IMPORTANT NOTICE: This web application is developed as a proof-of-concept prototype. The information provided here is NOT intended for actual usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.
        
        Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.
        
        Always consult with qualified professionals for accurate and personalized advice.
        ''')

    name_input = st.text_input("Please enter name and designation for email sign-off")
    st.session_state.name_input = name_input

    input_method = st.radio("Choose input method: ", ("Text Input", "Email Upload (.msg file):"))

    if input_method == "Text Input":
        text_input = st.text_area("Paste the content of the email below.", height = 300)    
        if st.button('Submit', type="primary"):
            public_query, email_elements = text_import(text_input)
            st.session_state.public_query = public_query
            st.session_state.email_elements = email_elements
            st.session_state.page = 'output'
            st.rerun()
        else:
             st.warning("Please provide an input before submitting")
    else: 
        email_input = st.file_uploader('Please upload an email message to submit')
        if email_input is not None:
            public_query, email_elements = email_msg_import(email_input)
            st.session_state.public_query = public_query
            st.session_state.email_elements = email_elements
            st.session_state.page = 'output'
            st.rerun()

elif st.session_state.page == 'output':
    st.title("Email Content and Response")
    
    st.subheader("Original Email Content:")
    st.write(st.session_state.public_query)
    
    st.subheader("Generated Response:")
    response = process_user_message_wq(st.session_state.public_query)
    st.write(response)
    
    # if st.button('Generate Email Template'):
    #     st.session_state.response = response
    #     st.session_state.page = 'download'
    #     st.rerun()
    
    if st.button('Back to Input'):
        st.session_state.page = 'input'
        st.rerun()
