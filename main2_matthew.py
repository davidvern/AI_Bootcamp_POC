# Set up and run this Streamlit App
import streamlit as st
from helper_functions import llm # <--- This is the helper function that we have created 🆕
from water_quality_query_handler import process_user_message_wq

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("Streamlit App")

form = st.form(key="form")
form.subheader("Prompt")

user_prompt = form.text_area("Enter your prompt here", height=200)

if form.form_submit_button("Submit"):
    st.toast(f"User Input Submitted - {user_prompt}")
    response = process_user_message_wq(user_prompt) #<--- This calls the `process_user_message` function that we have created 🆕
    st.write(response)
    print(f"User Input is {user_prompt}")