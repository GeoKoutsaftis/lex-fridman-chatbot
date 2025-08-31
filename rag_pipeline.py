
# rag_pipeline.py

import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from openai import OpenAI

PINECONE_API_KEY = "YOUR_PINECONE_API_KEY"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
INDEX_NAME = "lex-fridman-podcast"
EMBED_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "gpt-4o"

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)
embedder = SentenceTransformer(EMBED_MODEL)
client = OpenAI()

def retrieve_context(query, top_k=3):
    q_emb = embedder.encode([query])[0].tolist()
    results = index.query(vector=q_emb, top_k=top_k, include_metadata=True)
    context = "\n".join([m["metadata"]["text"] for m in results["matches"]])
    return context

def generate_answer(query):
    context = retrieve_context(query)
    prompt = f"""
    You are a helpful assistant answering questions about the Lex Fridman Podcast.
    Use ONLY the following context to answer the question.
    If the answer isn't in the context, say "I don't know."

    Context:
    {context}

    Question: {query}
    """
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or 'quit'): ")
        if q.lower() == "quit":
            break
        print(f"\nAnswer: {generate_answer(q)}\n")
