# main file to be run by streamlit.
# Set up and run this Streamlit App
import streamlit as st
import random  
import hmac  

from helper_functions.utility import check_password
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


st.title("Streamlit App")

form = st.form(key="form")
form.subheader("Prompt")

user_prompt = form.text_area("Enter your prompt here", height=100)

if form.form_submit_button("Submit"):
    st.toast(f"User Input Submitted - {user_prompt}")
    response = 'placeholder output' # <--- This calls the helper function that we have created 🆕
    st.write(response) # <--- This displays the response generated by the LLM onto the frontend 🆕
    print(f"User Input is {user_prompt}")
    print(response)

begin = st.container() 

if st.button('Clear name'): 
	st.session_state.name = '' 
	
if st.button('Streamlit!'): 
	st.session_state.name = ('Streamlit') 
	
# The widget is second in logic, but first in display 
begin.text_input('Name', key='name')