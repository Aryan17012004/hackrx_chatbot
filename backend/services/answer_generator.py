from typing import List, Dict
from backend.services.llm_models.openrouter import generate_openrouter_answer
from backend.models.schema import AnswerDetail

def generate_answer(question: str, relevant_chunks: List[Dict]) -> AnswerDetail:
    context = "\n\n".join([chunk["text"] for chunk in relevant_chunks])
    prompt = f"""
You are a legal and policy assistant AI. Use the context to answer the question.

Context:
{context}

Question:
{question}

Respond in JSON like:
{{
  "decision": "yes|no|depends",
  "answer": "...",
  "confidence_score": float,
  "reasoning": "..."
}}
"""
    llm_response = generate_openrouter_answer(prompt)
    try:
        return AnswerDetail(**llm_response)
    except:
        return AnswerDetail(decision="depends", answer="Parse error", confidence_score=0.0, reasoning="Invalid JSON")
