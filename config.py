import os

# Suppress Hugging Face symlink warning on Windows
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Ollama settings
MODEL_NAME = "llama3.2:3b"
OLLAMA_SYSTEM_PROMPT = (
    "You are Jarvis, a highly advanced, intelligent, and slightly sarcastic AI assistant. "
    "Keep your answers short, concise, and helpful. Act like the JARVIS from Iron Man."
)

# Wake Word Settings
# Default pre-trained model in openwakeword is 'hey_jarvis'.
