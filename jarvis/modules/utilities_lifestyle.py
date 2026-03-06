from __future__ import annotations

import threading
import time
from datetime import datetime

import requests

from jarvis.modules import base_actions as act
from jarvis.utils.logging_utils import action_guard

MODULE = "Utilities & Lifestyle"


def _extract_number(text: str, default: int = 5) -> int:
    for token in text.split():
        if token.isdigit():
            return int(token)
    return default


@action_guard(MODULE)
def weather(*, core, transcript: str) -> None:
    api_key = core.config.get("openweather_api_key")
    city = core.config.get("city", "London")
    if not api_key:
        core.speak("Weather API key missing.")
        return
    r = requests.get("https://api.openweathermap.org/data/2.5/weather", params={"q": city, "appid": api_key, "units": "metric"}, timeout=10)
    data = r.json()
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    core.speak(f"Weather in {city}: {temp}°C, {desc}.")


@action_guard(MODULE)
def crypto(*, core, transcript: str) -> None:
    coin = "bitcoin" if "bitcoin" in transcript else "ethereum"
    r = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids": coin, "vs_currencies": "usd"}, timeout=10)
    usd = r.json()[coin]["usd"]
    core.speak(f"{coin} is {usd} dollars.")


@action_guard(MODULE)
def currency(*, core, transcript: str) -> None:
    r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)
    eur = r.json()["rates"]["EUR"]
    core.speak(f"One dollar equals {eur:.2f} euro.")


@action_guard(MODULE)
def set_timer(*, core, transcript: str) -> None:
    seconds = _extract_number(transcript, default=10)

    def _alarm() -> None:
        core.speak(f"Timer finished: {seconds} seconds.")

    threading.Timer(seconds, _alarm).start()
    core.speak(f"Timer set for {seconds} seconds.")


@action_guard(MODULE)
def alarm(*, core, transcript: str) -> None:
    core.speak("Alarm feature armed. Use external scheduler for exact time triggers.")


@action_guard(MODULE)
def daily_news(*, core, transcript: str) -> None:
    act.open_url("https://www.bbc.com/news")
    core.speak("Opening your daily news briefing.")


@action_guard(MODULE)
def take_note(*, core, transcript: str) -> None:
    stamp = datetime.now().strftime("note_%Y%m%d_%H%M%S")
    note = transcript.replace("take note", "").strip() or "Voice note"
    path = act.create_note(stamp, note)
    core.speak(f"Note saved to {path.name}.")


@action_guard(MODULE)
def system_time(*, core, transcript: str) -> None:
    core.speak(datetime.now().strftime("Time is %H:%M"))


@action_guard(MODULE)
def stopwatch(*, core, transcript: str) -> None:
    start = time.time()
    core.runtime["stopwatch_start"] = start
    core.speak("Stopwatch started.")


@action_guard(MODULE)
def stopwatch_stop(*, core, transcript: str) -> None:
    start = core.runtime.get("stopwatch_start")
    if not start:
        core.speak("Stopwatch was not started.")
        return
    elapsed = time.time() - start
    core.speak(f"Stopwatch: {elapsed:.1f} seconds.")


def register(registry) -> None:
    registry.register("weather", ["weather", "current weather", "weather report", "temperature outside", "forecast now"], MODULE, weather)
    registry.register("crypto", ["crypto price", "bitcoin price", "ethereum price", "coin market", "digital currency price"], MODULE, crypto)
    registry.register("currency", ["currency rate", "dollar to euro", "exchange rate", "convert currency", "forex quote"], MODULE, currency)
    registry.register("timer", ["set timer", "start timer", "timer for", "countdown", "remind me in"], MODULE, set_timer)
    registry.register("alarm", ["set alarm", "alarm for tomorrow", "wake me up", "schedule alarm", "create alarm"], MODULE, alarm)
    registry.register("news", ["daily news", "news briefing", "morning headlines", "latest news", "open news"], MODULE, daily_news)
    registry.register("note", ["take note", "write note", "new note", "save memo", "remember this"], MODULE, take_note)
    registry.register("time", ["what time is it", "current time", "tell time", "clock now", "time check"], MODULE, system_time)
    registry.register("stopwatch_start", ["start stopwatch", "begin stopwatch", "track time", "start chronometer", "run stopwatch"], MODULE, stopwatch)
    registry.register("stopwatch_stop", ["stop stopwatch", "end stopwatch", "stop timing", "finish chronometer", "read stopwatch"], MODULE, stopwatch_stop)
    registry.register("social_x", ["open x", "open twitter", "twitter quick action", "go to x social", "social x"], MODULE, lambda **k: act.open_url("https://x.com"))
    registry.register("social_linkedin", ["open linkedin", "linkedin feed", "professional network", "go linkedin", "social linkedin"], MODULE, lambda **k: act.open_url("https://www.linkedin.com"))
    registry.register("social_instagram", ["open instagram", "instagram feed", "go instagram", "social instagram", "launch instagram"], MODULE, lambda **k: act.open_url("https://www.instagram.com"))
    registry.register("social_facebook", ["open facebook", "facebook feed", "go facebook", "social facebook", "launch facebook"], MODULE, lambda **k: act.open_url("https://www.facebook.com"))
    registry.register("quick_break", ["start break", "break timer", "focus break", "pomodoro break", "rest reminder"], MODULE, lambda core, transcript: set_timer(core=core, transcript="timer 300"))
