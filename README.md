# JARVIS Voice Assistant (Windows)

Professional-grade modular voice assistant using a registry architecture, fuzzy NLU, and threaded background listening.

## Features
- Registry pattern with scalable command modules.
- Fuzzy matching using Levenshtein ratio (>70 threshold).
- Threaded speech listener to avoid blocking.
- STT via `SpeechRecognition` (Google/Azure) and offline TTS via `pyttsx3`.
- Decorator-based logging and error safety.
- Safety protocol phrase: **"Jarvis, Override"**.
- 100+ voice aliases spanning Windows automation, media, internet/work, and utilities.

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python -m jarvis.main
```

## Notes
- Built for Windows hotkeys and app workflows.
- Many commands are scaffolded with robust logging and can be extended by plugging in real integrations.
