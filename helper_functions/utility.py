import streamlit as st  
import hmac  
import extract_msg
import email
import io

# """  
# This file contains the common components used in the Streamlit App.  
# This includes the sidebar, the title, the footer, and the password check.  
# """  

def check_password():  
    """Returns `True` if the user had the correct password."""  
    def password_entered():  
        """Checks whether a password entered by the user is correct."""  
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):  
            st.session_state["password_correct"] = True  
            del st.session_state["password"]  # Don't store the password.  
        else:  
            st.session_state["password_correct"] = False  
    # Return True if the passward is validated.  
    if st.session_state.get("password_correct", False):  
        return True  
    # Show input for password.  
    st.text_input(  
        "Password", type="password", on_change=password_entered, key="password"  
    )  
    if "password_correct" in st.session_state:  
        st.error("😕 Password incorrect")  
    return False

def print_header_if_exists(email_object, header_name):
    value = email_object.get(header_name)
    if value is not None:
        st.write(f'{header_name}: {value}')

def text_import(text_input):

    input_msg = email.message_from_string(text_input)

    # Reinstate below portion if we want to display none when para is not available.

    # st.write(f'Subject: {input_msg["Subject"]}')
    # st.write(f'From: {input_msg["From"]}')
    # st.write(f'To: {input_msg["To"]}')
    # st.write(f'CC: {input_msg.get("CC","N/A")}')
    # st.write(f'Date: {input_msg["Date"]}')

    print_header_if_exists(input_msg,'Subject')
    print_header_if_exists(input_msg,'From')
    print_header_if_exists(input_msg,'To')
    print_header_if_exists(input_msg,'CC')
    print_header_if_exists(input_msg,'Date')


    st.write("Body")
    if input_msg.is_multipart():
        for part in input_msg.walk():
            if part.get_content_type == 'text/plain':
                st.text(part.get_payload(decode=True).decode())

    else:
        st.write(input_msg.get_payload(decode=True).decode())
    
    # Extract email body for input into the LLM. 
    return input_msg.get_payload(decode=True).decode()


def email_msg_import(raw_msg):
    
    # reading the file
    raw_data = raw_msg.read()

    # parsing the message file
    msg_file = extract_msg.Message(io.BytesIO(raw_data))

    st.write(f'Subject: {msg_file.subject}')
    st.write(f'From: {msg_file.sender}')
    st.write(f'To: {msg_file.to}')
    st.write(f'CC: {msg_file.cc}')
    st.write(f'Date: {msg_file.date}')

    st.write("Body")
    st.write(f'Body: {msg_file.body}')
    
    msg_file.close()

    # Extract email body for input into the LLM.
    return msg_file.body