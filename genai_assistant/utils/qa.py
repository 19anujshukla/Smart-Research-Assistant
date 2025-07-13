import os
import faiss
import numpy as np
import cohere
from dotenv import load_dotenv

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# ✅ Create FAISS vector store using Cohere embeddings
def create_vector_store(text, chunk_size=150):  # reduce chunk size
    # Break text into chunks
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    # ✅ Limit total number of chunks (e.g., 100) to stay within token limit
    chunks = chunks[:100]

    # Get embeddings from Cohere
    response = co.embed(
        texts=chunks,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    embeddings = np.array(response.embeddings).astype("float32")

    # Create FAISS index
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(embeddings)

    return index, chunks

# ✅ Retrieve most relevant chunks
def get_relevant_chunks(question, index, chunks, k=3):
    q_embedding = co.embed(
        texts=[question],
        model="embed-english-v3.0",
        input_type="search_query"
    ).embeddings

    _, top_indices = index.search(np.array(q_embedding).astype("float32"), k)
    return [chunks[i] for i in top_indices[0]]

# ✅ Generate answer using context
def ask_with_context(question, context_chunks):
    context = "\n\n".join(context_chunks)
    prompt = f"""Answer the question using only the following context. Justify your answer briefly from the text.

Context:
{context}

Question: {question}
Answer:"""

    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=300,
        temperature=0.3
    )
    return response.generations[0].text.strip()
