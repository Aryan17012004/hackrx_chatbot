from pydantic import BaseModel
from typing import List

class AnswerDetail(BaseModel):
    decision: str
    answer: str
    confidence_score: float
    reasoning: str

class HackRxResponse(BaseModel):
    answers: List[AnswerDetail]