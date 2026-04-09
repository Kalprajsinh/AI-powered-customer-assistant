import os
import redis
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_redis import RedisChatMessageHistory

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

def get_redis_history(session_id: str):
    return RedisChatMessageHistory(
        session_id=session_id,
        redis_client=redis_client
    )

def ask_question(client, vector_store, query, session_id: str = "test_1"):

    # 🔍 Retrieve context
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(query)

    context = "\n\n".join([doc.page_content for doc in docs]) if docs else "No relevant context found."

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are an AI assistant specializing in MG Motor cars. Your role is to help customers by:
- Recommending cars based on their needs (family, budget, features, etc.)
- Providing detailed information about pricing, features, and specifications
- Answering FAQs about MG cars, booking, service, and charging infrastructure
- Giving accurate information from the provided knowledge base.

Use the following context to answer the user's question. If you don't know the answer, say so honestly.

Context:
{context}"""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])

    chain = prompt_template | client

    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_redis_history,
        input_messages_key="question",
        history_messages_key="history",
    )

    response = chain_with_history.invoke(
        {"question": query, "context": context},
        config={"configurable": {"session_id": session_id}},
    )

    return {
        "result": response.content,
        # "result": response,
        "source_documents": docs,
        "prompt": query
    }

# def ask_question(client, vector_store, query):

#     retriever = vector_store.as_retriever(search_kwargs={"k": 5})
#     docs = retriever.invoke(query)

#     context = "\n\n".join([doc.page_content for doc in docs])

#     prompt = f"""You are an AI assistant specializing in MG Motor cars. Your role is to help customers by:
# - Recommending cars based on their needs (family, budget, features, etc.)
# - Providing detailed information about pricing, features, and specifications
# - Answering FAQs about MG cars, booking, service, and charging infrastructure
# - Giving accurate information from the provided knowledge base.

# Use the following context to answer the user's question. If you don't know the answer, say so honestly.

# Context:
# {context}

# Question: {query}

# Answer as a helpful car advisor:"""

#     # completion = client.chat.completions.create(
#     #     model="llama-3.3-70b-versatile",
#     #     messages=[
#     #         {"role": "system", "content": "You are an expert MG car advisor."},
#     #         {"role": "user", "content": prompt}
#     #     ],
#     #     temperature=0.7,
#     #     max_completion_tokens=1024,
#     # )
#     response = client.invoke(prompt)

#     return {
#         # "result": completion.choices[0].message.content,
#         "result": response,
#         "source_documents": docs,
#         "prompt": prompt
#     }

    