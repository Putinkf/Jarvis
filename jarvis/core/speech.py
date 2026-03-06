from __future__ import annotations

import threading
import time
from collections.abc import Callable

import pyttsx3
import speech_recognition as sr

from jarvis.utils.logging_utils import logger


class SpeechService:
    def __init__(self, stt_backend: str = "google") -> None:
        self.engine = pyttsx3.init()
        self._configure_voice()
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.stt_backend = stt_backend.lower()

    def _configure_voice(self) -> None:
        voices = self.engine.getProperty("voices")
        preferred = None
        for voice in voices:
            descriptor = f"{voice.name} {voice.id}".lower()
            if "male" in descriptor and (
                "russian" in descriptor
                or "ru" in descriptor
                or "brit" in descriptor
                or "en-gb" in descriptor
            ):
                preferred = voice.id
                break
        if preferred:
            self.engine.setProperty("voice", preferred)
        self.engine.setProperty("rate", 176)

    def speak(self, text: str) -> None:
        logger.info("TTS: %s", text)
        self.engine.say(text)
        self.engine.runAndWait()

    def transcribe(self, audio: sr.AudioData) -> str:
        if self.stt_backend == "azure":
            try:
                return self.recognizer.recognize_azure(audio, language="ru-RU")
            except Exception:  # noqa: BLE001
                return self.recognizer.recognize_azure(audio, language="en-US")

        try:
            return self.recognizer.recognize_google(audio, language="ru-RU")
        except sr.UnknownValueError:
            return self.recognizer.recognize_google(audio, language="en-US")


class BackgroundListener:
    def __init__(self, speech: SpeechService, callback: Callable[[str], None]) -> None:
        self.speech = speech
        self.callback = callback
        self._stop_event = threading.Event()
        self.thread: threading.Thread | None = None

    def start(self) -> None:
        if self.thread and self.thread.is_alive():
            return
        self.thread = threading.Thread(target=self._run, daemon=True, name="jarvis-listener")
        self.thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self.thread:
            self.thread.join(timeout=2)

    def _run(self) -> None:
        with self.speech.mic as source:
            self.speech.recognizer.adjust_for_ambient_noise(source)
        while not self._stop_event.is_set():
            try:
                with self.speech.mic as source:
                    audio = self.speech.recognizer.listen(source, timeout=1, phrase_time_limit=6)
                text = self.speech.transcribe(audio).strip()
                if text:
                    logger.info("STT: %s", text)
                    self.callback(text)
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                logger.info("Речь не распознана")
            except Exception as exc:  # noqa: BLE001
                logger.exception("Ошибка фонового слушателя: %s", exc)
                time.sleep(0.4)
