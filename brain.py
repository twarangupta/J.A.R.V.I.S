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
        ]

    def ask(self, question: str) -> str:
        """
        Sends the question along with context history to the local Ollama instance
        and returns the AI's spoken response.
        """
        self.history.append({"role": "user", "content": question})
        try:
            response = ollama.chat(
                model=self.model,
                messages=self.history
            )
            reply = response.get("message", {}).get("content", "")
            if not reply:
                reply = "I apologize, but I received empty telemetry from my brain core."
            
            self.history.append({"role": "assistant", "content": reply})
            return reply
            
        except Exception as e:
            error_msg = f"Brain communication error: {e}"
            print(f"[Error] {error_msg}")
            # Do not append error message to history to keep it clean
            return "I am having trouble accessing my local cognitive models. Please verify Ollama is active."

# Singleton instance
brain = Brain()

def ask_ai(question: str) -> str:
    """Convenience helper to ask the brain."""
    return brain.ask(question)
