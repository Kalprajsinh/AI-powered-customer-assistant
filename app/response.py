def ask_question(client, vector_store, query):

    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""You are an AI assistant specializing in MG Motor cars. Your role is to help customers by:
- Recommending cars based on their needs (family, budget, features, etc.)
- Providing detailed information about pricing, features, and specifications
- Answering FAQs about MG cars, booking, service, and charging infrastructure
- Giving accurate information from the provided knowledge base.

Use the following context to answer the user's question. If you don't know the answer, say so honestly.

Context:
{context}

Question: {query}

Answer as a helpful car advisor:"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert MG car advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_completion_tokens=1024,
    )

    return {
        "result": completion.choices[0].message.content,
        "source_documents": docs,
        "prompt": prompt
    }

    