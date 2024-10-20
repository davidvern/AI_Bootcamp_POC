import os
import streamlit as st
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate

# Set up the OpenAI API key by setting the OPENAI_API_KEY environment variable
if load_dotenv('.env'):
   # for local development
   OPENAI_KEY = os.getenv('OPENAI_API_KEY')
else:
   OPENAI_KEY = st.secrets['OPENAI_API_KEY']

os.environ["OPENAI_API_KEY"] = OPENAI_KEY

# Checking for presence of basic vectordb
if os.path.exists('data\\basic_chroma_langchain_db'):
   print('Loading existing vector database.')
else:
   import rag_prep
   print('Vector database directory not found, proceeding to create vector datase.')
   rag_prep()

# Define embeddings model
embeddings_model = OpenAIEmbeddings(model = 'text-embedding-3-small',show_progress_bar=True)

# Load vector database from persistent directory
vectordb = Chroma(persist_directory='data/basic_chroma_langchain_db', embedding_function=embeddings_model)

f'Collection count for vector db is {vectordb._collection.count()}'

# Basic retrieval
qa_chain = RetrievalQA.from_chain_type(
   ChatOpenAI(model='gpt-4o-mini'),
   retriever=vectordb.as_retriever(k=20)
)

print(qa_chain.invoke("What is the safe level for e coli in drinking water?"))
print(qa_chain.invoke("What is the guideline values for dichlorobenzene in drinking water?"))

# Build prompt
template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use five sentences maximum. Cite the relevant sections where possible. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

# Run chain
qa_chain2 = RetrievalQA.from_chain_type(
    ChatOpenAI(model='gpt-4o-mini'),
    retriever=vectordb.as_retriever(k=20),
    return_source_documents=True, # Make inspection of document possible
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

print(qa_chain2.invoke("What is the guideline values for uranium in drinking water?"))