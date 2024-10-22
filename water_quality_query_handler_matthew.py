# This script contains a list of functions shown the cells below:
# 1. identify_water_quality parameter
# 2. match with PUB water quality standards and regulatory guidelines
# 3. Extract information from previous email archives
# 4. generate_response_based_on_water_quality_standards

from helper_functions import llm
from helper_functions.llm import get_completion_by_messages
import os
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import OutlookMessageLoader
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_experimental.text_splitter import SemanticChunker
from langchain.chains import RetrievalQA

# Import the data file in csv format
import pandas as pd
import json
# Convert .csv table into pandas Dataframe
water_quality_df = pd.read_csv('data/utf8_Consolidated WQ Parameters.csv')
parameter_list = water_quality_df['Parameter List'].tolist()

# Test Query Loop
# user_input = 'What is the pH and colour in PUB water?'

# 1. identify_water_quality parameter

def identify_water_quality_parameter(user_message):
    delimiter = "####"

    system_message = f"""
    You will be provided with water quality queries. \
    The water quality query will be enclosed in
    the pair of {delimiter}.

    Decide if the query contains any specific parameters from the 'Parameter List' column in the below Dataframe.
  
    {parameter_list}
    
    If there are any relevant parameters found, output the names into a list. 
    If are no relevant parameters are found, output an empty list.
    Would you like to make another enquiry?".

    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]
    output_step_1 = get_completion_by_messages(messages)
    output_step_1 = eval(output_step_1)
    return output_step_1 

# result_step_1 = identify_water_quality_parameter(user_input)
# print(result)

# 2. match with PUB water quality standards and regulatory guidelines
def get_water_quality_guidelines(list_of_water_quality_parameters: list):
    wq_parameter_guidelines = water_quality_df[water_quality_df['Parameter List'].isin(list_of_water_quality_parameters)]
    wq_parameter_guidelines = wq_parameter_guidelines.to_markdown()
    return wq_parameter_guidelines

# result_step_2 = get_water_quality_guidelines(result_step_1)

#3. Extract information from previous email archives

def extract_email_information(user_message):
# embedding model that we will use for the session
    embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')
# llm to be used in RAG pipeplines in this notebook
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0, seed=42)
# Use .listdir() method to list all the files and directories of a specified location
    directory = os.listdir('data/Queries Received and Email Responses')
# Empty list which will be used to append new values
    list_of_emails = []

    for filename in directory:
        filename = "data" + '/' + 'Queries Received and Email Responses' + '/' + filename
        loader = OutlookMessageLoader(filename)
        text_from_file = loader.load()
        # append the text from the single file to the existing list
        list_of_emails.append(text_from_file[0])
        # print(f"Successfully read from {filename}")
# Create the text splitter
    text_splitter = SemanticChunker(embeddings_model)
# Split the documents into smaller chunks
    splitted_documents = text_splitter.split_documents(list_of_emails)
# Create Vector Database
    vectordb = Chroma.from_documents(filter_complex_metadata(splitted_documents), embeddings_model, collection_name='embedding_semantic', persist_directory='./vector_db')
# Create RAG Chain
    retriever_chain_from_llm = RetrievalQA.from_llm(
        retriever=vectordb.as_retriever(), llm=llm
    )
    output_step_3 = retriever_chain_from_llm.invoke(user_message)
    return output_step_3

# result_step_3 = extract_email_information(user_input)

#4. Get relevant email records

def get_email_records(user_message):
# embedding model that we will use for the session
    embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')
# Use .listdir() method to list all the files and directories of a specified location
    directory = os.listdir('data/Queries Received and Email Responses')
# Empty list which will be used to append new values
    list_of_emails = []

    for filename in directory:
        filename = "data" + '/' + 'Queries Received and Email Responses' + '/' + filename
        loader = OutlookMessageLoader(filename)
        text_from_file = loader.load()
        # append the text from the single file to the existing list
        list_of_emails.append(text_from_file[0])
        # print(f"Successfully read from {filename}")
# Create the text splitter
    text_splitter = SemanticChunker(embeddings_model)
# Split the documents into smaller chunks
    splitted_documents = text_splitter.split_documents(list_of_emails)
# Create Vector Database
    vectordb = Chroma.from_documents(filter_complex_metadata(splitted_documents), embeddings_model, collection_name='embedding_semantic', persist_directory='./vector_db')
    output_step_4 = vectordb.similarity_search_with_relevance_scores(user_message, k=4)
    return output_step_4

# result_step_4 = get_email_records(user_input)

# 5. generate_response_based_on_water_quality_standards

def generate_response_based_on_water_quality_standards(user_message, water_quality_parameters, relevant_email, email_archives):
    delimiter = "####"

    system_message = f"""
    Follow these steps to answer the customer queries.
    The customer query will be delimited with a pair {delimiter}.

    Step 1:{delimiter} If the user is is asking about water quality, \
    understand the relevant parameter(s) from the 'Parameter List' column in table below:
    {water_quality_parameters}

    Step 2:{delimiter} Present the water quality parameters (listed in Step 1) and PUB Drinking Water Standard\
    in table format. The water quality parameters must be on the first column, with 'PUB Drinking Water Standard Average' \
    and 'PUB Drinking Water Standard Range' on subsequent columns. \
    Do not make comparisons between 'PUB Drinking Water Standard Range' and 'PUB Drinking Water Standard Average'.
    State the WHO Guidelines and EPH Regulations for the parameters, assure water is safe for drinking. \
    You must only rely on figures from the table. 
    
    Step 3:{delimiter}: Combine with the outputs from {relevant_email} where relevant. If the user message does not \
    contain water quality parameters, reply using content from {email_archives}.  
    Answer the customer in a friendly tone. \
    Do not make comparisons between 'PUB Drinking Water Standard Range' and 'PUB Drinking Water Standard Average'. \
    Make sure the statements are factually accurate. \
    Avoid repeating points from Step 2.
    Use Neural Linguistic Programming to construct your response.

    Use the following format:
    {delimiter} <Water quality table & Reasoning>
    {delimiter} <response to customer>

    Make sure to include {delimiter} to separate every step.
    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]

    response_to_customer = get_completion_by_messages(messages)
    # response_to_customer = response_to_customer.split(delimiter)[-1]
    return response_to_customer

# response = generate_response_based_on_water_quality_standards(user_input,result_step_2,result_step_3,result_step_4)
# print(response)

def process_user_message_wq(user_input):
    delimiter = "```"

    # Process 1. identify_water_quality parameter
    process_step_1 = identify_water_quality_parameter(user_input)

    # Process 2: Match with PUB water quality standards and regulatory guidelines
    process_step_2 = get_water_quality_guidelines(process_step_1)

    # Process 3: Match with PUB water quality standards and regulatory guidelines
    process_step_3 = extract_email_information(user_input)

    # Process 4: Match with PUB water quality standards and regulatory guidelines
    process_step_4 = get_email_records(user_input)

    # Process 5: Generate Response based on Course Details
    reply = generate_response_based_on_water_quality_standards(user_input,process_step_2,process_step_3,process_step_4)

    return reply