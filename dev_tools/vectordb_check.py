# This python serves as test area for various mechanisms to check for the presence of vector DBs
import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb

embeddings_model = OpenAIEmbeddings(model = 'text-embedding-3-small',show_progress_bar=True)

script_path = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_path)
email_persist_directory = os.path.join(root_dir,'data\\vectordb_email_semantic')
if os.path.exists(email_persist_directory):
    print(f'vectordb_email_semantic exists')
    vectordb_email= Chroma(
        persist_directory=email_persist_directory,
        collection_name='email_semantic',
        embedding_function=embeddings_model
    )
    print(f'Collection count = {len(vectordb_email.get()["documents"])}') # Should be 267
else:
    print(f'vectordb_email_semantic does not exist')

PUBFAQ_persist_directory = os.path.join(root_dir,'data\\PUB_FAQ_collection')
if os.path.exists(email_persist_directory):
    print(f'PUB_FAQ Collection exists')
    vectordb_faq = Chroma(
        persist_directory=PUBFAQ_persist_directory,
        collection_name='PUB_FAQ_collection',
        embedding_function=embeddings_model
    )
    print(f'Collection count = {len(vectordb_faq.get()["documents"])}') # Should be 99
else:
    print(f'PUB_FAQ_collection does not exist')