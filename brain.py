import ollama
from config import MODEL_NAME, OLLAMA_SYSTEM_PROMPT

class Brain:
    """
    Manages the offline conversation brain powered by Ollama.
    Maintains dialogue history to support continuous conversational context.
    """
    def __init__(self):
        self.model = MODEL_NAME
