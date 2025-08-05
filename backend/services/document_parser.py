import os, re, fitz, docx
from typing import Union, List
import dateparser

def parse_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return "\n\n".join(page.get_text() for page in fitz.open(path))
    if ext == ".docx":
        return "\n\n".join(p.text for p in docx.Document(path).paragraphs if p.text.strip())
    raise ValueError("Unsupported file format")

def chunk_text(text: str, chunk_size=500, overlap=50) -> List[str]:
    sents = re.split(r'(?<=[\.!?]) +', text)
    chunks, i = [], 0
    while i < len(sents):
        chunk, j = "", i
        while j < len(sents) and len(chunk) + len(sents[j]) < chunk_size:
            chunk += sents[j] + " "
            j += 1
        chunks.append(chunk.strip())
        i = max(j - overlap, i + 1)
    return chunks

def parse_and_chunk_document(path: Union[str, List[str]]) -> List[dict]:
    text = parse_file(path)
    chunks = chunk_text(text)
    return [{"id": f"chunk_{i}", "text": ch} for i, ch in enumerate(chunks)]