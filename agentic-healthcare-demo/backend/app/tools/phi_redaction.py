import re
def minimize_phi(text: str):
    text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]", text)
    return text, {"redactions": 1}
