from groq import Groq
# from langchain_community.llms import Ollama
from dotenv import load_dotenv
import os

load_dotenv()

def create_qa_client():
    
    api_key = os.getenv("GROQ_API_KEY")

    client = Groq(api_key=api_key)
    return client
    
    # return Ollama(model="qwen2.5:0.5b")