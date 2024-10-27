import sys
import os

module_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'logics')
sys.path.append('module_path')

from logics.email_query_handler import intermediate_response

initial_response_result = {
        "water quality": 'true',
        "water testing request": 'True',
        "product claim": 'TRUE'
    }

public_query = [] # find placeholder for query.

intermediate_response(public_query,initial_response_result)