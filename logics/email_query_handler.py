# Rough strucure of logic for the program

# Take in user query from the body of the email
# Determine the the nature of the email. Possible options include water quality query, request for testing and product advertisement claim
# As a first pass, assume that every email has  single topic, as an alternative an out a dictionary object where the type fo query is indicated as a boolean.
# stretch goal: include an other flag that will trigger a workflow that will feed the balance part of the email into more generic prompt

import json
from helper_functions import llm

def initial_response(public_query):
    delimiter = "###"

    system_message = f"""
    You are a customer service representative who is tasked to answer queries from members of the public.
    The query from the member of public will be delimited with a pair of {delimiter}. Use the following steps:

    Step 1: {delimiter} Categorize the query into the following categories: water quality, water testing request and product claim.
    Output a dictionary object, where each item is a key value pair where the key is the category and the value 
    is a Boolean value that is True if the category is relevant to query and False if it is not relevant.

    Ensure your response contains only the list of dictionary objects or an empty list without any emclosing tags or delimiters.
    """

    messages = [
        {'role': 'system',
         'content': system_message},
         {'role': 'user',
          'content': f"{delimiter}{public_query}{delimiter}"},
    ]

    query_catergory_result = llm.get_completion_by_messages(messages)
    query_catergory_result = query_catergory_result.replace("'", "\"")
    query_catergory_result = json.loads(query_catergory_result)[0]
    return query_catergory_result