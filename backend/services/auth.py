import os
from fastapi import Header, HTTPException

EXPECTED_TOKEN = os.getenv("HACKRX_API_KEY")

def get_token_header(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid format")
    token = authorization.split(" ")[1]
    if token != EXPECTED_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
    return token