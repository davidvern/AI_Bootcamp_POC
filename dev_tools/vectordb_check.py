# This python serves as test area for various mechanisms to check for the presence of vector DBs
import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb

script_path = os.path.dirname(os.path.abspath(__file__)) # current directory
root_dir = os.path.dirname(script_path) # one level higher
embeddings_model = OpenAIEmbeddings(model = 'text-embedding-3-small',show_progress_bar=True)
persist_directory = os.path.join(root_dir,'data\\vectordb_email_semantic') #navigate over to data folder

vectordb = Chroma(
    persist_directory=persist_directory,
    collection_name="email_semantic",
    embedding_function=embeddings_model
)

print(f"Vectorstore collection count: {len(vectordb.get()['documents'])}")

# logic flow for multi database 
# check for presence of directory, if exists probe further for collection, if it doesn't create the vectordb 
# if 