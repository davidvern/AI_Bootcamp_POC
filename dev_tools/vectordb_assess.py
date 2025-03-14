# This file will contain tools and functions that will be used to assess and troubleshoot the various aspects of the POC.
# functions and scripts in this folder will no be used in the main implementatio of the his POC.

import chromadb
import os

def verify_chroma_collection(collection):
  # verify contents of ChromaDB collection.
  items = collection.get()
  print(f"Number of items in collection: {len(items['ids'])}")
  print(f"Number of unique IDs: {len(set(items['ids']))}")
  if items['embeddings'] is None:
    print('Embeddings dimension is None type')
  else:
    print(f"Embedding dimension: {len(items['embeddings'])}")

  # print a few samples documents
  for i in range(min(5,len(items['documents']))):
    print(f"Sample document {i}: {items['documents'][i][:100]}...")

# Obtain current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to main directory
root_dir = os.path.dirname(current_dir)

# construct path to the vectordb folder

persist_directory = os.path.join(root_dir,'data\\vectordb_wq_reference')

client = chromadb.PersistentClient(path = persist_directory)

list_of_collections = client.list_collections()

print(list_of_collections)
print(list_of_collections[-1].name)
collection = client.get_collection(list_of_collections[-1].name)
verify_chroma_collection(collection)

# chroma utils vacuum --path data\vectordb_email_semantic_98 in command line to clean database.
# chroma utils vacuum --path data\vectordb_wq_reference      