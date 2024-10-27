# Rough strucure of logic for the program

# Take in user query from the body of the email
# Determine the the nature of the email. Possible options include water quality query, request for testing and product advertisement claim
# As a first pass, assume that every email has  single topic, as an alternative an out a dictionary object where the type fo query is indicated as a boolean.
# stretch goal: include an other flag that will trigger a workflow that will feed the balance part of the email into more generic prompt

import json
from helper_functions import llm
from logics.water_quality_query_handler_matthew import process_user_message_wq

def initial_response(public_query):
    # The role of this function is to take in the public_query (in the context of this script, it is the body of the email query).
    # The output for this function is a dictionary object indicating the type of the qiery classification for the use of the 
    # intermediate function
    delimiter = "###"

    system_message = f"""
    You are a customer service AI tasked with categorizing public queries. Follow these instructions precisely:
    1. The public's query will be delimited by `{delimiter}`.

    2. Identify the relevance of the query to each of these categories:
    - "water quality"
    - "water testing request"
    - "product claim"

    3. Output a JSON object with Boolean values (True or False) for each category, indicating relevance to the query. 
    Each key in the JSON object represents a category, and its corresponding value should be `True` if relevant, `False` if not.
    Example Response Format:
    ```json
    {{
        "water quality": True,
        "water testing request": False,
        "product claim": False
    }}
    """

    messages = [
        {'role': 'system',
         'content': system_message},
         {'role': 'user',
          'content': f"{delimiter}{public_query}{delimiter}"},
    ]

    query_category_result = llm.get_completion_by_messages(messages,json_output=True)
    query_category_result = json.loads(query_category_result)
    return query_category_result

def intermediate_response(public_query,query_category_result):
    # run through the various scenarios and obtain the responses for the various scenarios.
    # pre-allocate repose items
    water_quality_response = []
    water_testing_response = []
    product_quality_response = []
    if query_category_result['water quality']:
        # pass into water_quality_handler.py
        print('True for water_quality testing category')
        water_quality_response = process_user_message_wq(public_query)       

    if query_category_result['water testing request']:
        print('True for water testing request')
        water_testing_response = water_testing_query_handler(public_query)

    if query_category_result['product claim']:
        print('True for product claim query')
        pass
        
    return water_quality_response, water_testing_response, product_quality_response

def water_testing_query_handler(public_query):
    # This query serves as a simple branch to reject queries enquire whether PUB provide a service to test water quality.
    delimiter = "###"
    system_message = f"""
    You are a customer service AI tasked with addressing queries on whether the company offers testing of water samples as a service.
    This is a service that our company does not offer.
    As a result, your role is to take in the public query delimited by `{delimiter}` and draft a polite response stating that the 
    Public Utilities Board (PUB) does not offer water quality testing as a service.

    Your respose should only address this aspect of the public query. The response should be one paragraph consisting of at most 3 sentences.
    """
    messages = [
        {'role':'system',
         'content':system_message},
         {'role':'user',
          'content':f"{delimiter}{public_query}{delimiter}"}
    ]

    water_testing_query_response = llm.get_completion_by_messages(messages)
    return water_testing_query_response

# def product_claim_query_handler(public_query):
    # This query serves to address non-parameter water quality related concerns that can be addressed from the FAQ on the PUB website.
    # this script will need a RAG framework

def full_worflow(public_query):
    
    query_category = initial_response(public_query)

    a,b,c = intermediate_response(public_query,query_category)
   
    return [a,b,c]