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
# Set to 'hey_jarvis' or path to custom trained 'daddy_s_home.tflite' model.
WAKE_WORD_MODEL = "hey_jarvis" 
WAKE_WORD_THRESHOLD = 0.2

# Sleep trigger phrase
SLEEP_WORD = "go to sleep"

# Speech-to-Text Settings (Faster Whisper)
WHISPER_MODEL_SIZE = "small"  # Options: tiny, base, small, medium, large-v3 or local folder path
WHISPER_DEVICE = "cpu"        # GTX 1650 doesn't have PyTorch CUDA, so we use cpu
