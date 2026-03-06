from __future__ import annotations

import json
import threading
from pathlib import Path

from jarvis.core.registry import CommandRegistry
from jarvis.core.speech import BackgroundListener, SpeechService
from jarvis.modules import internet_work, system_hardware, utilities_lifestyle, yandex_music
from jarvis.utils.logging_utils import logger


class Core:
    OVERRIDE_PHRASE = "jarvis override"

    def __init__(self, config_path: str = "config.json") -> None:
        self.config = self._load_config(config_path)
        self.runtime: dict[str, float] = {}
        self.registry = CommandRegistry(threshold=70)
        self.speech = SpeechService(stt_backend=self.config.get("stt_backend", "google"))
        self.listener = BackgroundListener(self.speech, self.process_transcript)
        self._running = threading.Event()
        self._cancel = threading.Event()
        self._exec_lock = threading.Lock()
        self._register_all()

    def _load_config(self, path: str) -> dict:
        file = Path(path)
        if not file.exists():
            return {}
        try:
            return json.loads(file.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            return {}

    def _register_all(self) -> None:
        yandex_music.register(self.registry)
        system_hardware.register(self.registry)
        internet_work.register(self.registry)
        utilities_lifestyle.register(self.registry)

    def speak(self, text: str) -> None:
        self.speech.speak(text)

    def confirm(self, prompt: str) -> bool:
codex/create-modular-voice-assistant-jarvis-0b32yk
        self.speak(f"{prompt}. Скажите 'да', чтобы продолжить, сэр."
        return True

    def start(self) -> None:
        self._running.set()
codex/create-modular-voice-assistant-jarvis-0b32yk
        self.speak("JARVIS активирован и готов к работе, сэр.")
        self.listener.start()
        try:
            while self._running.is_set():
                threading.Event().wait(0.2)
        finally:
            self.listener.stop()

    def stop(self) -> None:
        self._running.clear()

    def override(self) -> None:
        self._cancel.set()
codex/create-modular-voice-assistant-jarvis-0b32yk
        self.speak("Протокол Override принят. Останавливаю текущие задачи, сэр.")

    def process_transcript(self, transcript: str) -> None:
        text = transcript.lower().strip()
        if self.OVERRIDE_PHRASE in text or "джарвис отмена" in text or "джарвис стоп" in text:
            self.override()
            return

        self._cancel.clear()
        cmd, score, alias = self.registry.match(text)
        if not cmd:
codex/create-modular-voice-assistant-jarvis-0b32yk
            logger.info("Команда не распознана: '%s' (score=%s)", transcript, score)
            return

        if self._cancel.is_set():
            return

codex/create-modular-voice-assistant-jarvis-0b32yk
        logger.info("Совпадение '%s' с алиасом '%s' (%s%%)", cmd.name, alias, score)

        with self._exec_lock:
            if self._cancel.is_set():
                return
            cmd.handler(core=self, transcript=transcript)
