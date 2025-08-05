# backend/state/session.py

# ------------------------------
# ✅ Simple in-memory state store
# ------------------------------
session_state = {
    "file_path": None,          # last ingested document
    "selected_model": "openrouter"  # default model
}

def get_state(key: str):
    return session_state.get(key)

def set_state(key: str, value):
    session_state[key] = value

def clear_state():
    session_state.clear()
