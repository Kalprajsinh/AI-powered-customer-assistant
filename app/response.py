import os
import redis
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_redis import RedisChatMessageHistory

redis_url = os.getenv("REDIS_URL")
 
if redis_url:
    redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
else:
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
        ("system", """You are a professional AI assistant specializing in MG Motor vehicles.

    Your responsibilities:
    - Recommend suitable MG cars based on customer needs (budget, family size, usage, city/highway driving, EV preference, etc.)
    - Provide accurate and detailed information on pricing, variants, features, specifications, mileage, and comparisons
    - Answer FAQs related to MG cars, booking process, service, warranty, and charging infrastructure (for EVs)
    - Guide users in decision-making in a clear, helpful, and structured way

    Guidelines:
    - Always be polite, concise, and informative
    - Ask follow-up questions if user requirements are unclear
    - Prefer structured answers (bullet points, sections) when explaining features or comparisons
    - Do NOT make up information — only use the provided context
    - If information is missing, say: "I don't have that information right now"
    - Highlight key selling points clearly when recommending a car

    Response Style:
    - Start with a direct answer or recommendation
    - Then provide supporting details (features, specs, price range, etc.)
    - Keep explanations simple and user-friendly (avoid overly technical language unless asked)

    Context:
    {context}
    """),
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

    