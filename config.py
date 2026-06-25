import os

# Suppress Hugging Face symlink warning on Windows
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Load environment variables from .env if python-dotenv is installed
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except ImportError:
    pass

# Ollama settings
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_SYSTEM_PROMPT = (
    "You are Jarvis, a highly advanced, intelligent, and slightly sarcastic AI assistant. "
    "Keep your answers short, concise, and helpful. Act like the JARVIS from Iron Man.\n\n"
    "CRITICAL ROUTING RULES:\n"
    "If the user is asking you to perform a system action or run a git command, you MUST prepend your message with exactly `[COMMAND: <command_name>]` before any conversational text. Choose ONLY from the following valid command names:\n"
    "- For stashing: `[COMMAND: git stash]`\n"
    "- For stashing pop: `[COMMAND: git stash pop]`\n"
    "- For pulling: `[COMMAND: git pull]`\n"
    "- For pushing: `[COMMAND: git push]`\n"
    "- For status: `[COMMAND: git status]`\n"
    "- For committing: `[COMMAND: git commit]`\n"
    "- For checking merge conflicts: `[COMMAND: git conflicts]`\n"
    "- For viewing logs/commits history: `[COMMAND: git log]`\n"
    "- For switching/checking out branch: `[COMMAND: switch branch to <branch_name>]` (replace <branch_name> with target branch)\n"
    "- For listing branches: `[COMMAND: git branch]`\n"
    "- For organizers: `[COMMAND: organize downloads]`\n"
    "- For locking system: `[COMMAND: lock pc]`\n"
    "- For volume adjustment: `[COMMAND: volume up]` or `[COMMAND: volume down]` or `[COMMAND: mute]` or `[COMMAND: unmute]`\n\n"
    "Formatting examples:\n"
    "- User: 'put my current work on hold' -> '[COMMAND: git stash] I have stashed your changes, sir.'\n"
    "- User: 'sync with the remote origin' -> '[COMMAND: git pull] Syncing latest updates, sir.'\n"
    "- User: 'bring back my stashes' -> '[COMMAND: git stash pop] Restoring changes, sir.'\n"
    "Do NOT invent new commands or use other formatting styles like [JARVIS] or [Hgit pull]. If the request is just conversational, output NO command tag."
)

# Wake Word Settings
# Default pre-trained model in openwakeword is 'hey_jarvis'.
# Set to 'hey_jarvis' or path to custom trained 'daddy_s_home.tflite' model.
WAKE_WORD_MODEL = os.getenv("WAKE_WORD_MODEL", "hey_jarvis")
WAKE_WORD_THRESHOLD = float(os.getenv("WAKE_WORD_THRESHOLD", "0.2"))

# Sleep trigger phrase
SLEEP_WORD = os.getenv("SLEEP_WORD", "go to sleep")

# Speech-to-Text Settings (Faster Whisper)
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base")  # Options: tiny, base, small, medium, large-v3 or local folder path
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")        # GTX 1650 doesn't have PyTorch CUDA, so we use cpu
WHISPER_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8") # int8 is recommended for CPU speed when using small/medium models
WHISPER_LANGUAGE = os.getenv("WHISPER_LANGUAGE", "en")       # Lock speech detection to English to prevent hallucinations from noise
WHISPER_VAD_FILTER = os.getenv("WHISPER_VAD_FILTER", "True").lower() in ("true", "1", "yes")

# Text-to-Speech Settings (pyttsx3)
VOICE_RATE = int(os.getenv("VOICE_RATE", "170"))
VOICE_VOLUME = float(os.getenv("VOICE_VOLUME", "1.0"))
VOICE_INDEX = int(os.getenv("VOICE_INDEX", "0")) # 0 for male, 1 for female (depends on system voices installed)

# Audio Settings
SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", "16000")) # Required by OpenWakeWord and Whisper
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1280"))    # 80ms chunk size for 16kHz audio