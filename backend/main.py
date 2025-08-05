import os
import tempfile
import requests
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from backend.services.embedder import ingest_document
from backend.services.retriever import retrieve_chunks
from backend.services.answer_generator import generate_answer
from backend.services.auth import get_token_header
from backend.models.schema import AnswerDetail, HackRxResponse

load_dotenv()
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class HackRxRequest(BaseModel):
    document_url: str
    questions: List[str]

@app.post("/api/v1/hackrx/run", response_model=HackRxResponse)
async def run_hackrx_endpoint(payload: HackRxRequest, token: str = Depends(get_token_header)):
    try:
        response = requests.get(payload.document_url, timeout=10)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download doc")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(response.content)
            file_path = tmp.name
        doc_chunks = ingest_document(file_path)
        answers = []
        for q in payload.questions:
            top_chunks = retrieve_chunks(q, doc_chunks)
            answers.append(generate_answer(q, top_chunks))
        return HackRxResponse(answers=answers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
