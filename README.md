# Offline-Pi-AI-Voice - Offline AI Voice Assistant for Raspberry Pi
An offline, AI-powered voice assistant designed to run locally on Raspberry Pi 5. Pi-AI-Voice combines speech recognition, a lightweight Large Language Model (LLM), and text-to-speech to provide a local voice interaction experience without depending on cloud AI services.

**Your voice. Your AI. Your device. No cloud required.**

## ✨ Features

- 🎤 **Voice Input:** Capture voice commands through a microphone.
- 📝 **Speech Recognition:** Convert speech into text using Whisper.cpp.
- 🧠 **Local AI Intelligence:** Generate responses using Qwen2.5 through llama.cpp.
- 🔊 **Text-to-Speech:** Convert AI responses into spoken audio using Piper.
- 🔒 **Privacy First:** Audio and conversations are processed locally.
- 🌐 **Offline Operation:** No internet connection required during normal operation after downloading models and dependencies.
- 🚀 **Automatic Startup:** Run the assistant automatically when Raspberry Pi boots.
- 🐧 **Linux Based:** Built using Python and optimized for Raspberry Pi.

## 🏗️ Architecture

```text
             USER
               |
               v
        +--------------+
        |  Microphone  |
        +--------------+
               |
               v
        +--------------+
        | Audio Capture|
        +--------------+
               |
               v
        +--------------+
        | Whisper.cpp  |
        | Speech to    |
        | Text (STT)   |
        +--------------+
               |
               v
        +--------------+
        | Python       |
        | Assistant    |
        +--------------+
               |
               v
        +--------------+
        | llama.cpp    |
        | Qwen2.5 LLM  |
        +--------------+
               |
               v
        +--------------+
        | AI Response  |
        +--------------+
               |
               v
        +--------------+
        | Piper TTS    |
        | Text to      |
        | Speech       |
        +--------------+
               |
               v
        +--------------+
        | Speaker      |
        +--------------+
```

## 🖥️ Hardware Requirements

| Component | Specification |
|---|---|
| Computer | Raspberry Pi 5 |
| RAM | 2 GB (minimum target configuration) |
| Storage | 64 GB microSD |
| Power Supply | Official Raspberry Pi 27W USB-C supply recommended |
| Microphone | USB microphone |
| Speaker | USB or Bluetooth speaker |
| Network | Required for initial downloads; not required for normal offline operation |

## 🧰 Software Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Speech Recognition | Whisper.cpp |
| AI Inference Engine | llama.cpp |
| Language Model | Qwen2.5-0.5B-Instruct |
| Model Format | GGUF |
| Model Quantization | Q4_0 |
| Text-to-Speech | Piper |
| Operating System | Raspberry Pi OS / compatible Linux |
| Audio | ALSA / PipeWire |

## 🤖 AI Models

### 1. Speech Recognition – Whisper

Model: `tiny.en`

Repository: https://github.com/ggml-org/whisper.cpp

### 2. Language Model – Qwen2.5

Model: `Qwen2.5-0.5B-Instruct`

Quantization: `Q4_0`

Model download:

https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF

Recommended model file:

`qwen2.5-0.5b-instruct-q4_0.gguf`

### 3. Text-to-Speech – Piper

Voice: `en_US-lessac-medium`

Repository:

https://github.com/rhasspy/piper

## 📁 Project Structure

```text
Pi-AI-Voice/
│
├── main.py
├── config.py
│
├── models/
│   └── qwen2.5-0.5b-instruct-q4_0.gguf
│
├── voices/
│   ├── en_US-lessac-medium.onnx
│   └── en_US-lessac-medium.onnx.json
│
├── audio/
│
├── whisper.cpp/
│   ├── build/
│   └── models/
│       └── ggml-tiny.en.bin
│
├── llama.cpp/
│   └── build/
│
├── env/
│
└── README.md
```

### 1. Build Whisper.cpp

```bash
git clone https://github.com/ggml-org/whisper.cpp.git

cd whisper.cpp
cmake -B build
cmake --build build -j2
cd ..
```

### 2. Download the English tiny model:

```bash
cd whisper.cpp
bash ./models/download-ggml-model.sh tiny.en
cd ..
```

### 3. Build llama.cpp

```bash
git clone https://github.com/ggml-org/llama.cpp.git

cd llama.cpp
cmake -B build
cmake --build build -j2
cd ..
```

Download the Qwen2.5 GGUF model from Hugging Face and place it inside the `models/` directory.

### 4. Configure Piper

Download the Piper executable and the `en_US-lessac-medium` voice model.

Place the voice files inside:

```text
voices/
```

## ▶️ Start the assistant:

```bash
python main.py
```

The assistant is intended to capture voice input, transcribe it, generate a response using the local LLM, and speak the response through the configured audio output.

## 🔄 Automatic Startup Using systemd

To start app automatically when Raspberry Pi boots, create a service:

```bash
sudo nano /etc/systemd/system/Pi-AI-Voice.service
```

Example service file (adjust the username and paths for your installation):

```ini
[Unit]
Description=Pi-AI-Voice Offline AI Voice Assistant
After=network.target

[Service]
Type=simple
User=YOUR_LINUX_USERNAME
WorkingDirectory=/home/YOUR_LINUX_USERNAME/Pi-AI-Voice
ExecStart=/home/YOUR_LINUX_USERNAME/Pi-AI-Voice/env/bin/python -u main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable Pi-AI-Voice
sudo systemctl start Pi-AI-Voice
```

Check service status:

```bash
sudo systemctl status Pi-AI-Voice
```

View live logs:

```bash
sudo journalctl -u Pi-AI-Voice -f
```

## ⚡ Performance Optimization

Raspberry Pi 5 with 2 GB RAM has limited resources. The project targets lightweight models and sequential inference.

Suggested starting settings:

| Parameter | Suggested Value |
|---|---|
| LLM | Qwen2.5 0.5B |
| Quantization | Q4_0 |
| Context Size | 512–1024 |
| CPU Threads | 2 |
| Whisper Model | tiny.en |
| Maximum Response Tokens | 100 |

Avoid running multiple AI inference processes simultaneously.

## 🔐 Privacy

Pi-AI-Voice is designed around local processing:

- Voice recognition runs locally.
- Language generation runs locally.
- Text-to-speech runs locally.
- No cloud AI API is required for normal operation.

Model downloads and initial software installation require internet access.

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.
Feel free to fork the repository, submit issues, and create pull requests.
