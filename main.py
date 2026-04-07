from app.load_document import load_documents
from app.vector_store import get_vector_store
from app.llm_client import create_qa_client
from app.response import ask_question
import os

def main():

    persist_dir = "./faiss_db"

    print("Setting up AI agent...")
    vector_store = get_vector_store(persist_dir)

    print("Creating GenAI client...")
    client = create_qa_client()

    print("AI Agent ready! You can now ask questions about MG cars.")

    # Example queries
    example_queries = [
        "What are the features of MG Hector?",
        "How much does MG Gloster cost?",
        "What is the booking process for MG cars?",
        "Tell me about MG's charging infrastructure",
        "Recommend a car for family use"
    ]

    print("\nExample queries you can ask:")
    for query in example_queries:
        print(f"- {query}")

    session_id = "test_1"  
    while True:
        query = input("\nAsk a question (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break

        try:
            result = ask_question(client, vector_store, query, session_id=session_id)
            print(f"\nAnswer: {result['result']}")
            # print(f"\nSources: {[doc.metadata['source'] for doc in result['source_documents']]}")
            print('=='*24)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()