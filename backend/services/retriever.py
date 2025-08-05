import numpy as np
import faiss
from typing import List, Dict
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_chunks(query: str, doc_chunks: List[Dict], top_k: int = 5) -> List[Dict]:
    texts = [c["text"] for c in doc_chunks]
    embeddings = model.encode(texts).astype("float32")
    q_emb = model.encode([query]).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    _, indices = index.search(q_emb, min(top_k, len(doc_chunks)))
    return [doc_chunks[i] for i in indices[0]]