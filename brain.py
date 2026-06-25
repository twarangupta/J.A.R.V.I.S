import ollama
from config import MODEL_NAME, OLLAMA_SYSTEM_PROMPT

class Brain:
    """
    Manages the offline conversation brain powered by Ollama.
    Maintains dialogue history to support continuous conversational context.
    """
    def __init__(self):
        self.model = MODEL_NAME
        self.system_prompt = OLLAMA_SYSTEM_PROMPT
        self.history = []
        self.reset_conversation()

    def reset_conversation(self):
        """Resets conversational memory and injects the system prompt."""
        self.history = [
            {"role": "system", "content": self.system_prompt}
