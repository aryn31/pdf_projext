from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

model = SentenceTransformer("all-MiniLM-L6-v2")
dimension = 384
index = faiss.IndexFlatL2(dimension)

def embed_and_store(chunks):
    embeddings = model.encode(chunks)
    index.reset()
    index.add(np.array(embeddings).astype("float32"))

def search_similar_chunks(question, k=3):
    q_embedding = model.encode([question]).astype("float32")
    _, I = index.search(q_embedding, k)
    return I[0]
