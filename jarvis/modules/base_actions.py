from __future__ import annotations

import os
import subprocess
import webbrowser
from pathlib import Path

import psutil

try:
    import pyautogui
except Exception:  # noqa: BLE001
    pyautogui = None


def hotkey(*keys: str) -> None:
    if pyautogui:
        pyautogui.hotkey(*keys)


def press(key: str) -> None:
    if pyautogui:
        pyautogui.press(key)


def typewrite(text: str) -> None:
    if pyautogui:
        pyautogui.typewrite(text)


def launch(path_or_cmd: str) -> None:
    subprocess.Popen(path_or_cmd, shell=True)


def open_url(url: str) -> None:
    webbrowser.open(url)


def battery_report() -> str:
    battery = psutil.sensors_battery()
    if not battery:
        return "Battery info unavailable"
    state = "charging" if battery.power_plugged else "discharging"
    return f"Battery {battery.percent:.0f}% and {state}."


def cpu_ram_report() -> str:
    cpu = psutil.cpu_percent(interval=0.2)
    mem = psutil.virtual_memory().percent
    return f"CPU {cpu:.0f}% and RAM {mem:.0f}%."


def lock_screen() -> None:
    os.system("rundll32.exe user32.dll,LockWorkStation")


def create_note(name: str, text: str = "") -> Path:
    notes = Path.home() / "Documents" / "JarvisNotes"
    notes.mkdir(parents=True, exist_ok=True)
    target = notes / f"{name}.txt"
    target.write_text(text, encoding="utf-8")
    return target
