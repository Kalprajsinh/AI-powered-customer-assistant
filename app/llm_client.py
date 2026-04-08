# from groq import Groq
# from langchain_community.llms import Ollama
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()

def create_qa_client():
    
    api_key = os.getenv("GROQ_API_KEY")

    client = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        groq_api_key=api_key,
    )

    return client
    
    # return Ollama(model="qwen2.5:0.5b")