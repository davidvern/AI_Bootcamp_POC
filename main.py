# main file to be run by streamlit.
# Set up and run this Streamlit App
import streamlit as st
from helper_functions.utility import text_import 
from helper_functions.utility import email_msg_import
from helper_functions.utility import check_password
from logics.email_query_handler import full_worflow

# from logics.custom_query_handler import process_user_message  # placeholder to import logics function

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

st.title("Water Quality Email Response Generator")

if 'input_mode' not in st.session_state:
    st.session_state.llm_trigger = False

with st.expander('Click to see disclaimer'):
    st.write('''
    IMPORTANT NOTICE: This web application is developed as a proof-of-concept prototype. The information provided here is NOT intended for actual usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.
    
    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.
    
    Always consult with qualified professionals for accurate and personalized advice.
    ''')

# To consider adding in a fixed input for the name and designation of the officer to sign off the email.
name_input = st.text_input("Please enter name and designation for email sign-off")


# select input method for email, either by copy pasting the email body or via uploading of msg file.
input_method =  st.radio("Choose input method: ", ("Text Input", "Email Upload (.msg file):"))

if input_method == "Text Input":
    # Create input are for email body
    text_input = st.text_area("Paste the content of the email below.", height = 300)    
    if st.button('Submit',type="primary"):
        public_query = text_import(text_input)
        st.session_state.llm_trigger = True
    else:
         st.warning("Please provide an input before submitting")
else: 
    # if opt for .msg input
    email_input = st.file_uploader('Please upload an email message to submit')
    if email_input is not None:
        public_query = email_msg_import(email_input)
        st.session_state.llm_trigger = True

if st.session_state.llm_trigger:
    response = full_worflow(public_query)   
    st.write(response)