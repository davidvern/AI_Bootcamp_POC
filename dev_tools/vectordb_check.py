# This python serves as test area for various mechanisms to check for the presence of vector DBs
import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb

script_path = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_path)

persist_directory = os.path.join(root_dir,'data\\basic_chroma_langchain_db')

result = os.path.exists(persist_directory)
print(result)

client = chromadb.PersistentClient(path=persist_directory) #create chromadb from scratch
# check for presence of collection
coll = client.list_collections() # produces a list of chromadb.api.models.Collection.Collection
print(type(coll)) # list

print(client.get_collection('WQ_reference_material'))

# logic flow for multi database 
# check for presence of directory, if exists probe further for collection, if it doesn't create the vectordb 
# if 