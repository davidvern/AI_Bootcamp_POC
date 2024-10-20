def main():

    import os
    from langchain_community.document_loaders import PyPDFLoader

    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from helper_functions.llm import count_tokens

    from langchain_chroma import Chroma
    from langchain_openai import OpenAIEmbeddings

    loader_eph = PyPDFLoader('data\code-of-practice-on-drinking-water-sampling-and-safety-plans-sfa-apr-2019.pdf')
    doc_eph = loader_eph.load()

    loader_who = PyPDFLoader('data\WHO GDWQ 4th ed 1st 2nd addenda 2022-eng.pdf')
    doc_who = loader_who.load()

    loader_sfa = PyPDFLoader('data\Environmental Public Health (Water suitable for drinking)(No. 2) Regulations SFA Apr 2019.pdf')
    doc_sfa = loader_sfa.load()

    # Creating character splitter for document splitting and chunking
    splitter1 = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=500,
        chunk_overlap=50,
        length_function=count_tokens
    )

    split_eph = splitter1.split_documents(doc_eph)
    split_who = splitter1.split_documents(doc_who)
    split_sfa = splitter1.split_documents(doc_sfa)
    split_doc_merge = split_eph + split_who + split_sfa

    # Creating embedding model
    embeddings_model = OpenAIEmbeddings(model = 'text-embedding-3-small',show_progress_bar=True)

    # Creating basic vector database
    vector_store = Chroma.from_documents(
        collection_name="Basic_WQ_reference_material",
        documents=split_doc_merge,
        embedding=embeddings_model,
        persist_directory="data/basic_chroma_langchain_db",  # Where to save data locally, remove if not neccesary
    )

if __name__ == "__main__": 
	main()