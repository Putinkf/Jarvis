import ctypes
import json
import logging
import os
import subprocess
import sys
import threading
import time
import webbrowser
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import pyautogui
import pyttsx3
import speech_recognition as sr

try:
    import pygame
except Exception:  # noqa: BLE001
    pygame = None

try:
    import tkinter as tk
    from PIL import Image, ImageTk
except Exception:  # noqa: BLE001
    tk = None
    Image = None
    ImageTk = None


WAKE_WORD = "джарвис"
COMMANDS_PATH = Path("commands.json")
PROFANITIES = ["блять", "сука", "нахуй", "пиздец", "шлюха"]


@dataclass
class CommandEntry:
    category: str
    intent: str
    phrase: str


class CommandDatabase:
    """Generates and loads voice commands from JSON."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def ensure_exists(self) -> None:
        if self.path.exists():
            logging.info("Командная база уже существует: %s", self.path)
            return

        command_map = self._build_command_map()
        self.path.write_text(json.dumps(command_map, ensure_ascii=False, indent=2), encoding="utf-8")
        total_phrases = sum(
            len(intent_data["phrases"])
            for category_data in command_map.values()
            for intent_data in category_data.values()
        )
        logging.info("Создан файл команд: %s. Всего фраз: %s", self.path, total_phrases)

    def load_entries(self) -> List[CommandEntry]:
        data = json.loads(self.path.read_text(encoding="utf-8"))
        entries: List[CommandEntry] = []
        for category, intents in data.items():
            for intent, payload in intents.items():
                for phrase in payload.get("phrases", []):
                    entries.append(CommandEntry(category=category, intent=intent, phrase=phrase.lower()))
        logging.info("Загружено команд: %s", len(entries))
        return entries

    @staticmethod
    def _build_command_map() -> Dict[str, Dict[str, Dict[str, List[str]]]]:
        return {
            "system": {
                "volume_up": {
                    "phrases": [
                        "сделай громче",
                        "повысь громкость",
                        "добавь звук",
                        "увеличь громкость",
                        "громкость плюс",
                        "прибавь громкость",
                        "сделай звук громче",
                        "подними звук",
                        "увеличь звук",
                        "громче пожалуйста",
                    ]
                },
                "volume_down": {
                    "phrases": [
                        "сделай тише",
                        "уменьши громкость",
                        "убавь звук",
                        "понизь громкость",
                        "громкость минус",
                        "снизь громкость",
                        "сделай звук тише",
                        "опусти звук",
                        "убери громкость",
                        "тише пожалуйста",
                    ]
                },
                "mute": {
                    "phrases": [
                        "выключи звук",
                        "без звука",
                        "мут",
                        "отключи громкость",
                        "сделай беззвучно",
                        "поставь на беззвучный",
                        "тишина",
                        "mute",
                        "звук ноль",
                        "убери весь звук",
                    ]
                },
                "shutdown": {
                    "phrases": [
                        "выключи компьютер",
                        "заверши работу",
                        "отключи пк",
                        "выруби компьютер",
                        "пора выключаться",
                        "компьютер выключить",
                        "завершение работы",
                        "сделай выключение",
                        "полностью выключи",
                        "отключение системы",
                    ]
                },
                "sleep": {
                    "phrases": [
                        "усыпи компьютер",
                        "режим сна",
                        "отправь в сон",
                        "компьютер спать",
                        "включи спящий режим",
                        "пк в сон",
                        "сонный режим",
                        "переведи в сон",
                        "режим ожидания",
                        "усыпление системы",
                    ]
                },
                "restart": {
                    "phrases": [
                        "перезагрузи компьютер",
                        "сделай перезагрузку",
                        "рестарт системы",
                        "перезапусти пк",
                        "перезапуск компьютера",
                        "перезагрузка",
                        "уйди в ребут",
                        "перезапусти систему",
                        "ребут",
                        "перезапусти компьютер",
                    ]
                },
            },
            "apps": {
                "open_telegram": {
                    "phrases": [
                        "открой телеграм",
                        "запусти telegram",
                        "включи телегу",
                        "телеграм открыть",
                        "нужен telegram",
                    ]
                },
                "open_discord": {
                    "phrases": [
                        "открой дискорд",
                        "запусти discord",
                        "включи дискорд",
                        "дискорд открыть",
                        "нужен discord",
                    ]
                },
                "open_steam": {
                    "phrases": [
                        "открой стим",
                        "запусти steam",
                        "включи стим",
                        "стим открыть",
                        "нужен steam",
                    ]
                },
                "open_calculator": {
                    "phrases": [
                        "открой калькулятор",
                        "запусти калькулятор",
                        "калькулятор открыть",
                        "нужен калькулятор",
                        "включи calc",
                    ]
                },
                "open_notepad": {
                    "phrases": [
                        "открой блокнот",
                        "запусти блокнот",
                        "включи notepad",
                        "блокнот открыть",
                        "нужен блокнот",
                    ]
                },
            },
            "browser": {
                "open_youtube": {
                    "phrases": [
                        "открой ютуб",
                        "запусти youtube",
                        "перейди на youtube",
                        "включи ютуб",
                        "открой youtube сайт",
                    ]
                },
                "open_google": {
                    "phrases": [
                        "открой гугл",
                        "запусти google",
                        "перейди в google",
                        "включи поиск google",
                        "открой главную google",
                    ]
                },
                "open_vk": {
                    "phrases": [
                        "открой вк",
                        "запусти вконтакте",
                        "перейди в vk",
                        "включи вк",
                        "открой vk сайт",
                    ]
                },
                "open_github": {
                    "phrases": [
                        "открой гитхаб",
                        "запусти github",
                        "перейди на github",
                        "включи github",
                        "открой github сайт",
                    ]
                },
            },
            "pc_control": {
                "minimize_all": {
                    "phrases": [
                        "сверни все окна",
                        "покажи рабочий стол",
                        "минимизируй окна",
                        "свернуть всё",
                        "убери окна",
                    ]
                },
                "take_screenshot": {
                    "phrases": [
                        "сделай скриншот",
                        "сфотографируй экран",
                        "снимок экрана",
                        "захвати экран",
                        "скрин экрана",
                    ]
                },
                "press_enter": {
                    "phrases": [
                        "нажми enter",
                        "жми ввод",
                        "подтверди enter",
                        "кнопка enter",
                        "нажать ввод",
                    ]
                },
                "press_space": {
                    "phrases": [
                        "нажми пробел",
                        "жми space",
                        "кнопка пробел",
                        "нажать пробел",
                        "space нажми",
                    ]
                },
            },
            "dialogue": {
                "creator": {
                    "phrases": [
                        "кто твой создатель",
                        "кто тебя создал",
                        "кто сделал тебя",
                        "кто твой разработчик",
                        "кто тебя написал",
                    ]
                },
                "joke": {
                    "phrases": [
                        "расскажи анекдот",
                        "пошути",
                        "рассмеши меня",
                        "дай шутку",
                        "хочу анекдот",
                    ]
                },
                "inquisitor_mode": {
                    "phrases": [
                        "режим инквизитора",
                        "включи режим инквизитора",
                        "активируй инквизитора",
                        "запусти инквизитора",
                        "инквизитор",
                    ]
                },
            },
        }


class Inquisitor:
    def __init__(self, image_path: Path, audio_path: Path) -> None:
        self.image_path = image_path
        self.audio_path = audio_path
        self._lock = threading.Lock()

    def trigger(self) -> None:
        if not self._lock.acquire(blocking=False):
            logging.info("Инквизитор уже активен, повторный запуск пропущен.")
            return

        threading.Thread(target=self._run, daemon=True).start()

    def _run(self) -> None:
        try:
            logging.info("ИНКВИЗИТОР АКТИВИРОВАН")
            self._set_volume_100()
            self._play_audio()
            self._flash_window()
        except Exception:
            logging.exception("Ошибка в модуле инквизитора")
        finally:
            self._lock.release()

    @staticmethod
    def _set_volume_100() -> None:
        user32 = ctypes.windll.user32
        vk_volume_up = 0xAF
        for _ in range(60):
            user32.keybd_event(vk_volume_up, 0, 0, 0)
            user32.keybd_event(vk_volume_up, 0, 2, 0)
            time.sleep(0.01)

    def _play_audio(self) -> None:
        if not pygame:
            logging.error("pygame недоступен, аудио flashbang.mp3 не будет воспроизведено.")
            return
        if not self.audio_path.exists():
            logging.error("Аудиофайл не найден: %s", self.audio_path)
            return
        pygame.mixer.init()
        pygame.mixer.music.load(str(self.audio_path))
        pygame.mixer.music.play()

    def _flash_window(self) -> None:
        if not tk or not Image or not ImageTk:
            logging.error("Tkinter/Pillow недоступны, визуальная часть инквизитора пропущена.")
            time.sleep(3)
            return
        if not self.image_path.exists():
            logging.error("Изображение не найдено: %s", self.image_path)
            time.sleep(3)
            return

        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-topmost", True)

        image = Image.open(self.image_path)
        photo = ImageTk.PhotoImage(image)
        width, height = image.size

        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2

        root.geometry(f"{width}x{height}+{x}+{y}")
        label = tk.Label(root, image=photo, borderwidth=0, highlightthickness=0)
        label.image = photo
        label.pack()

        root.after(3000, root.destroy)
        root.mainloop()


class JarvisAssistant:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts = pyttsx3.init()
        self.tts.setProperty("rate", 170)
        self.db = CommandDatabase(COMMANDS_PATH)
        self.entries: List[CommandEntry] = []
        self.stop_background: Optional[Callable[..., Any]] = None
        self.command_lock = threading.Lock()
        self.inquisitor = Inquisitor(Path("jesus.jpg"), Path("flashbang.mp3"))

    def setup(self) -> None:
        logging.info("Инициализация Jarvis...")
        self.db.ensure_exists()
        self.entries = self.db.load_entries()
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        logging.info("Jarvis готов к работе.")

    def speak(self, text: str) -> None:
        logging.info("TTS: %s", text)
        self.tts.say(text)
        self.tts.runAndWait()

    def run(self) -> None:
        self.setup()
        self.stop_background = self.recognizer.listen_in_background(
            self.microphone,
            self._background_callback,
            phrase_time_limit=4,
        )

        logging.info("Фоновое прослушивание активировано.")
        self.speak("Джарвис в сети.")

        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            logging.info("Остановка по KeyboardInterrupt")
        finally:
            if self.stop_background:
                self.stop_background(wait_for_stop=False)

    def _background_callback(self, recognizer: sr.Recognizer, audio: sr.AudioData) -> None:
        try:
            text = recognizer.recognize_google(audio, language="ru-RU").lower().strip()
            logging.info("Распознано (фон): %s", text)
        except sr.UnknownValueError:
            logging.info("Речь не распознана (фон).")
            return
        except Exception:
            logging.exception("Ошибка распознавания фона")
            return

        if any(bad_word in text for bad_word in PROFANITIES):
            logging.warning("Обнаружена ненормативная лексика: %s", text)
            self.inquisitor.trigger()
            return

        if "режим инквизитора" in text and WAKE_WORD in text:
            self.inquisitor.trigger()
            return

        if WAKE_WORD not in text:
            return

        if not self.command_lock.acquire(blocking=False):
            logging.info("Командный канал занят. Wake word пропущен.")
            return

        threading.Thread(target=self._wake_command_flow, daemon=True).start()

    def _wake_command_flow(self) -> None:
        try:
            self._acknowledge()
            command = self._listen_for_command(timeout=5)
            if not command:
                self.speak("Не услышал команду.")
                return
            logging.info("Команда после wake word: %s", command)
            self._route_command(command)
        except Exception:
            logging.exception("Ошибка в потоке обработки команды")
        finally:
            self.command_lock.release()

    def _acknowledge(self) -> None:
        try:
            ctypes.windll.user32.MessageBeep(0xFFFFFFFF)
        except Exception:
            self.speak("Слушаю")
        else:
            self.speak("Да, сэр")

    def _listen_for_command(self, timeout: int = 5) -> str:
        with self.microphone as source:
            try:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=timeout)
            except sr.WaitTimeoutError:
                return ""
        try:
            return self.recognizer.recognize_google(audio, language="ru-RU").lower().strip()
        except sr.UnknownValueError:
            logging.info("Команда не распознана.")
            return ""
        except Exception:
            logging.exception("Ошибка распознавания команды")
            return ""

    def _route_command(self, command: str) -> None:
        if "включи" in command and len(command.split()) >= 2:
            maybe_query = self._extract_music_query(command)
            if maybe_query:
                self._handle_yandex_music(maybe_query)
                return

        matched = self._find_best_match(command)
        if not matched:
            self.speak("Команда не найдена.")
            return

        logging.info("Совпадение: %s/%s (%s)", matched.category, matched.intent, matched.phrase)
        self._execute_intent(matched.category, matched.intent)

    @staticmethod
    def _extract_music_query(command: str) -> Optional[str]:
        if not command.startswith("включи "):
            return None
        query = command.replace("включи", "", 1).strip()
        blocked_words = {"звук", "телеграм", "дискорд", "стим", "калькулятор", "блокнот"}
        if not query or query in blocked_words:
            return None
        return query

    def _find_best_match(self, command: str) -> Optional[CommandEntry]:
        best_entry: Optional[CommandEntry] = None
        best_ratio = 0.0

        for entry in self.entries:
            if entry.phrase in command or command in entry.phrase:
                return entry
            ratio = SequenceMatcher(None, command, entry.phrase).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_entry = entry

        return best_entry if best_entry and best_ratio >= 0.62 else None

    def _execute_intent(self, category: str, intent: str) -> None:
        handlers: Dict[Tuple[str, str], Callable[[], None]] = {
            ("system", "volume_up"): lambda: self._press_key("volumeup", 8, "Делаю громче"),
            ("system", "volume_down"): lambda: self._press_key("volumedown", 8, "Делаю тише"),
            ("system", "mute"): lambda: self._press_key("volumemute", 1, "Звук выключен"),
            ("system", "shutdown"): self._shutdown,
            ("system", "sleep"): self._sleep,
            ("system", "restart"): self._restart,
            ("apps", "open_telegram"): lambda: self._open_app("telegram", "Открываю Telegram"),
            ("apps", "open_discord"): lambda: self._open_app("discord", "Открываю Discord"),
            ("apps", "open_steam"): lambda: self._open_app("steam", "Открываю Steam"),
            ("apps", "open_calculator"): lambda: self._open_app("calc", "Открываю калькулятор"),
            ("apps", "open_notepad"): lambda: self._open_app("notepad", "Открываю блокнот"),
            ("browser", "open_youtube"): lambda: self._open_url("https://youtube.com", "Открываю YouTube"),
            ("browser", "open_google"): lambda: self._open_url("https://google.com", "Открываю Google"),
            ("browser", "open_vk"): lambda: self._open_url("https://vk.com", "Открываю ВК"),
            ("browser", "open_github"): lambda: self._open_url("https://github.com", "Открываю GitHub"),
            ("pc_control", "minimize_all"): self._minimize_all,
            ("pc_control", "take_screenshot"): self._take_screenshot,
            ("pc_control", "press_enter"): lambda: self._press_key("enter", 1, "Нажимаю Enter"),
            ("pc_control", "press_space"): lambda: self._press_key("space", 1, "Нажимаю пробел"),
            ("dialogue", "creator"): lambda: self.speak("Меня создал мой разработчик. Я служу вам, сэр."),
            ("dialogue", "joke"): lambda: self.speak("Почему программист перепутал Хэллоуин и Рождество? Потому что OCT 31 равно DEC 25."),
            ("dialogue", "inquisitor_mode"): self.inquisitor.trigger,
        }

        action = handlers.get((category, intent))
        if not action:
            self.speak("Для этой команды пока нет обработчика.")
            return

        try:
            action()
        except Exception:
            logging.exception("Ошибка при выполнении интента %s/%s", category, intent)
            self.speak("Произошла ошибка при выполнении команды.")

    def _handle_yandex_music(self, query: str) -> None:
        self.speak(f"Включаю {query}")
        try:
            result = subprocess.run("start yandexmusic://", shell=True, check=False)
            if result.returncode != 0:
                raise RuntimeError("Не удалось открыть yandexmusic://")
            time.sleep(2)
            pyautogui.hotkey("ctrl", "f")
            pyautogui.typewrite(query, interval=0.04)
            pyautogui.press("enter")
            logging.info("Yandex Music desktop flow выполнен для: %s", query)
        except Exception:
            logging.exception("Desktop Yandex Music не сработал. Переход в web fallback.")
            url = f"https://music.yandex.ru/search?text={query}"
            webbrowser.open(url)

    def _press_key(self, key: str, count: int, phrase: str) -> None:
        self.speak(phrase)
        for _ in range(count):
            pyautogui.press(key)

    def _open_app(self, command: str, phrase: str) -> None:
        self.speak(phrase)
        subprocess.Popen(f"start {command}", shell=True)

    def _open_url(self, url: str, phrase: str) -> None:
        self.speak(phrase)
        webbrowser.open(url)

    def _shutdown(self) -> None:
        self.speak("Выключаю компьютер")
        subprocess.Popen("shutdown /s /t 0", shell=True)

    def _sleep(self) -> None:
        self.speak("Перевожу компьютер в сон")
        subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)

    def _restart(self) -> None:
        self.speak("Перезагружаю компьютер")
        subprocess.Popen("shutdown /r /t 0", shell=True)

    def _minimize_all(self) -> None:
        self.speak("Сворачиваю все окна")
        pyautogui.hotkey("win", "d")

    def _take_screenshot(self) -> None:
        filename = f"screenshot_{int(time.time())}.png"
        pyautogui.screenshot(filename)
        self.speak("Скриншот сохранён")
        logging.info("Скриншот сохранён: %s", filename)


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(threadName)s | %(message)s",
        handlers=[
            logging.FileHandler("jarvis.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


if __name__ == "__main__":
    configure_logging()
    try:
        assistant = JarvisAssistant()
        assistant.run()
    except Exception:
        logging.exception("Критическая ошибка в Jarvis")
