# Voice-Enabled AI Assistant

A Python-based voice assistant that uses speech recognition and OpenAI's GPT to provide voice-based interactions.

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

1. Run the assistant:
```bash
python main.py
```

2. Speak into your microphone when prompted
3. Say "goodbye" or "exit" to end the conversation

## Features

- Voice input using sounddevice for audio capture
- Speech-to-text using Google Speech Recognition API
- AI responses using OpenAI's GPT-3.5
- Text-to-speech output using macOS's built-in 'say' command
- Conversation memory for context-aware responses

## Requirements

- Python 3.x
- macOS (for text-to-speech)
- Active OpenAI API key with available quota
- Microphone access
- Internet connection for Google Speech Recognition and OpenAI API 