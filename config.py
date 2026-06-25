import os

# Suppress Hugging Face symlink warning on Windows
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Ollama settings
MODEL_NAME = "llama3.2:3b"
