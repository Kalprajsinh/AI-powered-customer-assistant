
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document

from app.load_document import load_documents

def create_vector_store(documents: list[Document], persist_directory: str = "./faiss_db"):
   
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)

    # embeddings
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # vector store
    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vector_store

def get_vector_store(persist_directory: str = "./faiss_db"):
    
    if os.path.exists(persist_directory):
        print("Loading existing vector store...")
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = FAISS.load_local(persist_directory, embeddings)
    else:
        print("Creating new vector store...")
        data_folder = "Data"
        documents = load_documents(data_folder)
        print(f"Loaded {len(documents)} documents")
        vector_store = create_vector_store(documents, persist_directory)
    return vector_store