from typing import Dict, List

# Stores conversation history per phone number
# Format: { "whatsapp:+233xxxxxxx": [ {"role": "user", "content": "..."}, ... ] }
_sessions: Dict[str, List[dict]] = {}


def get_history(phone: str) -> List[dict]:
    """Return conversation history for a given phone number."""
    return _sessions.get(phone, [])


def add_message(phone: str, role: str, content: str) -> None:
    """Append a message to a user's conversation history."""
    if phone not in _sessions:
        _sessions[phone] = []
    _sessions[phone].append({"role": role, "content": content})


def clear_history(phone: str) -> None:
    """Clear conversation history (e.g. after order confirmed)."""
    _sessions.pop(phone, None)