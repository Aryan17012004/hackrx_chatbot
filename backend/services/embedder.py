import os
import faiss
import pickle
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from backend.services.document_parser import parse_and_chunk_document

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # ✅ Lightweight
VECTOR_DIR = "vector_db"
os.makedirs(VECTOR_DIR, exist_ok=True)

def embed_text(texts: List[str]) -> np.ndarray:
    return model.encode(texts, show_progress_bar=True).astype("float32")

def ingest_document(file_path: str) -> List[Dict]:
    doc_chunks = parse_and_chunk_document(file_path)
    texts = [c["text"] for c in doc_chunks]
    embeddings = embed_text(texts)
    for i, c in enumerate(doc_chunks):
        c["embedding"] = embeddings[i]
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, os.path.join(VECTOR_DIR, "index.faiss"))
    with open(os.path.join(VECTOR_DIR, "text.pkl"), "wb") as f:
        pickle.dump(doc_chunks, f)
    return doc_chunks