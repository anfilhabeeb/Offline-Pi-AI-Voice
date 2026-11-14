
from pathlib import Path

# Main project directory
BASE_DIR = Path(__file__).resolve().parent

# Whisper.cpp
WHISPER_BIN = (
    BASE_DIR / "whisper.cpp/build/bin/whisper-cli"
)

WHISPER_MODEL = (
    BASE_DIR / "whisper.cpp/models/ggml-tiny.en.bin"
)

# llama.cpp
LLAMA_BIN = (
    BASE_DIR / "llama.cpp/build/bin/llama-cli"
)

# Local AI model
LLM_MODEL = (
    BASE_DIR / "models/qwen2.5-0.5b-instruct-q4_0.gguf"
)

# Piper English voice
ENGLISH_VOICE = (
    BASE_DIR / "voices/en_US-lessac-medium.onnx"
)

# Audio
AUDIO_DIR = BASE_DIR / "audio"

RECORD_SECONDS = 7

# AI settings for Raspberry Pi 5 (2 GB)
MAX_TOKENS = 50
CONTEXT_SIZE = 1024

TEMPERATURE = 0.7
