import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
SITE_URL = os.getenv("SITE_URL", "https://your-site.com")
SITE_NAME = os.getenv("SITE_NAME", "Your App")

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": SITE_URL,
    "X-Title": SITE_NAME,
}


def generate_openrouter_answer(prompt: str, model_name: str = "deepseek/deepseek-chat-v3-0324") -> dict:
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a policy assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3
    }
    try:
        response = requests.post(OPENROUTER_API_URL, headers=HEADERS, data=json.dumps(payload))
        if response.status_code != 200:
            return {
                "decision": "depends",
                "answer": "LLM failed.",
                "confidence_score": 0.0,
                "reasoning": response.text,
            }
        content = response.json()["choices"][0]["message"]["content"]
        import re
        match = re.search(r"\{.*\}", content, re.DOTALL)
        return json.loads(match.group(0)) if match else {
            "decision": "depends",
            "answer": "Invalid format.",
            "confidence_score": 0.0,
            "reasoning": content,
        }
    except Exception as e:
        return {
            "decision": "depends",
            "answer": "Exception occurred.",
            "confidence_score": 0.0,
            "reasoning": str(e),
        }
