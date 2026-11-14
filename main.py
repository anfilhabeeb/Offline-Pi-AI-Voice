import subprocess
import sys
import re
from pathlib import Path
from config import *

def check_files():

    required = [
        WHISPER_BIN,
        WHISPER_MODEL,
        LLAMA_BIN,
        LLM_MODEL,
        ENGLISH_VOICE
    ]

    for file in required:
        if not file.exists():
            raise FileNotFoundError(
                f"Required file not found: {file}"
            )

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def run_command(command, timeout=300):

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=timeout
    )

    if result.returncode != 0:
        print("\nCommand failed:")
        print(result.stderr[-2000:])
        raise RuntimeError("Command execution failed")

    return result


def run_command_llm(command, timeout=300):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout
    )

    if result.returncode != 0:
        print("\nCommand failed:")
        print(result.stderr[-2000:])
        raise RuntimeError("Command execution failed")

    return result


def record_audio():

    audio_file = AUDIO_DIR / "recording.wav"

    print("\nListening... Speak now!")

    subprocess.run(
        [
            "arecord",
            "-D", "plughw:2,0",
            "-f", "S16_LE",
            "-r", "16000",
            "-c", "1",
            "-d", str(RECORD_SECONDS),
            str(audio_file)
        ],
        check=True
    )

    return audio_file


def speech_to_text(audio_file):

    print("\nRecognizing English speech...")

    output_prefix = AUDIO_DIR / "transcript"
    output_file = Path(str(output_prefix) + ".txt")

    if output_file.exists():
        output_file.unlink()

    run_command([
        str(WHISPER_BIN),
        "-m", str(WHISPER_MODEL),
        "-f", str(audio_file),
        "-l", "en",
        "-nt",
        "-np",
        "-otxt",
        "-of", str(output_prefix)
    ], timeout=180)

    if not output_file.exists():
        return ""

    text = output_file.read_text(
        encoding="utf-8"
    ).strip()

    print("\nYou:", text)

    return text


def generate_response(user_text, history):
    print("\nThinking...")

    system_prompt = """
    You are a helpful offline AI voice assistant.
    
    Rules:
    1. Always communicate in English.
    2. Give clear and concise answers.
    3. Keep answers suitable for spoken conversation.
    4. Avoid unnecessary long explanations.
    5. If you do not know something, say so.
    """

    conversation = (
        "<|im_start|>system\n"
        + system_prompt
        + "<|im_end|>\n"
    )

    for user, assistant in history:

        conversation += (
            f"<|im_start|>user\n{user}"
            f"<|im_end|>\n"
        )

        conversation += (
            f"<|im_start|>assistant\n{assistant}"
            f"<|im_end|>\n"
        )

    conversation += (
        f"<|im_start|>user\n{user_text}"
        f"<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )

    result = run_command_llm([
        str(LLAMA_BIN),
        "-m", str(LLM_MODEL),
        "-p", conversation,
        "-n", str(MAX_TOKENS),
        "-c", str(CONTEXT_SIZE),
        "--temp", str(TEMPERATURE),
        "--no-display-prompt",
        "--simple-io",
        "--single-turn"
    ], timeout=60)

    answer = result.stdout.strip()

    answer = re.split(r"<\|im_start\|>assistant\s*", answer)[-1]
    answer = re.split(r"<\|im_end\|>|\[ Prompt:", answer)[0].strip()

    if not answer:
        answer = "Sorry, I could not generate a response."

    return answer

def text_to_speech(text):

    if not text:
        return

    output_file = AUDIO_DIR / "response.wav"

    print("\nGenerating English voice...")

    run_command([
        sys.executable,
        "-m", "piper",
        "-m", str(ENGLISH_VOICE),
        "-f", str(output_file),
        "--",
        text
    ], timeout=180)

    print("Speaking...")

    subprocess.run(
        ["pw-play", str(output_file)],
        check=True
    )


def main():

    print("=" * 50)
    print(" RASPBERRY PI OFFLINE VOICE CHATBOT")
    print("=" * 50)

    print("Language       : English")
    print("Speech Engine  : Whisper.cpp")
    print("AI Model       : Qwen 0.5B")
    print("Voice Engine   : Piper")
    print("Mode           : Completely Offline")

    check_files()

    history = []

    while True:

        try:
            print("Listening...")

            input(
                "\nPress ENTER to speak "
                "(Ctrl+C to exit)..."
            )

            audio_file = record_audio()
            user_text = speech_to_text(audio_file)

            if not user_text:
                print("No speech recognized.")
                continue

            if user_text.lower().strip(
                " .!?"
            ) in ["exit", "quit", "stop"]:

                print("Exiting chatbot...")
                break

            answer = generate_response(
                user_text,
                history
            )

            history.append((user_text, answer))
            # Keep only the latest two exchanges
            history = history[-2:]

            history = []
            print(answer)

            text_to_speech(answer)

        except KeyboardInterrupt:
            break

        except Exception as e:
            print("\nError:", e)

    print("\nChatbot stopped.")

if __name__ == "__main__":
    main()



