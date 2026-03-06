from __future__ import annotations

import threading
import time
from datetime import datetime

import requests

from jarvis.modules import base_actions as act
from jarvis.utils.logging_utils import action_guard

MODULE = "Utilities & Lifestyle"


def aliases(ru: list[str], en: list[str]) -> list[str]:
    return ru + en


def _extract_number(text: str, default: int = 5) -> int:
    for token in text.split():
        if token.isdigit():
            return int(token)
    return default


@action_guard(MODULE)
def weather(*, core, transcript: str) -> None:
    api_key = core.config.get("openweather_api_key")
    city = core.config.get("city", "Moscow")
    if not api_key:
        core.speak("Сэр, ключ OpenWeather не задан.")
        return
    r = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "appid": api_key, "units": "metric", "lang": "ru"},
        timeout=10,
    )
    data = r.json()
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    core.speak(f"Сэр, погода в городе {city}: {temp}°C, {desc}.")


@action_guard(MODULE)
def crypto(*, core, transcript: str) -> None:
    coin = "bitcoin" if "биткоин" in transcript.lower() or "bitcoin" in transcript.lower() else "ethereum"
    r = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids": coin, "vs_currencies": "usd"},
        timeout=10,
    )
    usd = r.json()[coin]["usd"]
    core.speak(f"Сэр, текущая цена {coin}: {usd} долларов.")


@action_guard(MODULE)
def currency(*, core, transcript: str) -> None:
    r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)
    eur = r.json()["rates"]["EUR"]
    rub = r.json()["rates"]["RUB"]
    core.speak(f"Сэр, один доллар равен {eur:.2f} евро и {rub:.2f} рубля.")


@action_guard(MODULE)
def set_timer(*, core, transcript: str) -> None:
    seconds = _extract_number(transcript, default=10)

    def _alarm() -> None:
        core.speak(f"Сэр, таймер завершён. Прошло {seconds} секунд.")

    threading.Timer(seconds, _alarm).start()
    core.speak(f"Запускаю таймер на {seconds} секунд, сэр.")


@action_guard(MODULE)
def alarm(*, core, transcript: str) -> None:
    core.speak("Сэр, будильник отмечен. Для точного времени используйте планировщик задач.")


@action_guard(MODULE)
def daily_news(*, core, transcript: str) -> None:
    act.open_url("https://lenta.ru")
    core.speak("Открываю ежедневную новостную сводку, сэр.")


@action_guard(MODULE)
def take_note(*, core, transcript: str) -> None:
    stamp = datetime.now().strftime("note_%Y%m%d_%H%M%S")
    note = transcript.replace("заметка", "").replace("take note", "").strip() or "Голосовая заметка"
    path = act.create_note(stamp, note)
    core.speak(f"Сэр, заметка сохранена: {path.name}.")


@action_guard(MODULE)
def system_time(*, core, transcript: str) -> None:
    core.speak(datetime.now().strftime("Сэр, текущее время %H:%M"))


@action_guard(MODULE)
def stopwatch(*, core, transcript: str) -> None:
    core.runtime["stopwatch_start"] = time.time()
    core.speak("Сэр, секундомер запущен.")


@action_guard(MODULE)
def stopwatch_stop(*, core, transcript: str) -> None:
    start = core.runtime.get("stopwatch_start")
    if not start:
        core.speak("Сэр, секундомер ещё не был запущен.")
        return
    elapsed = time.time() - start
    core.speak(f"Сэр, секундомер: {elapsed:.1f} секунд.")


def register(registry) -> None:
    registry.register("weather", aliases(["погода", "какая погода", "прогноз", "температура", "погода сейчас", "погода на улице", "погодный отчёт"], ["weather", "current weather"]), MODULE, weather)
    registry.register("crypto", aliases(["курс крипты", "цена биткоина", "курс эфира", "криптовалюта", "цена криптовалюты", "биткоин цена", "ethereum price"], ["crypto price", "bitcoin price", "ethereum price"]), MODULE, crypto)
    registry.register("currency", aliases(["курс валют", "доллар в евро", "доллар в рубли", "обменный курс", "курс обмена", "конвертация валют", "валюта курс"], ["currency rate", "exchange rate"]), MODULE, currency)
    registry.register("timer", aliases(["поставь таймер", "запусти таймер", "таймер на", "обратный отсчёт", "напомни через", "таймер", "старт таймер"], ["set timer", "start timer", "countdown"]), MODULE, set_timer)
    registry.register("alarm", aliases(["поставь будильник", "будильник", "разбуди меня", "создай будильник", "утренний будильник", "alarm set", "план будильника"], ["set alarm", "create alarm"]), MODULE, alarm)
    registry.register("news", aliases(["новости", "сводка новостей", "утренние новости", "последние новости", "что в новостях", "новостной брифинг", "открой новости"], ["daily news", "news briefing"]), MODULE, daily_news)
    registry.register("note", aliases(["сделай заметку", "запиши заметку", "новая заметка", "сохрани заметку", "помни это", "note", "voice note"], ["take note", "write note"]), MODULE, take_note)
    registry.register("time", aliases(["который час", "текущее время", "скажи время", "время сейчас", "часы", "узнать время", "time now"], ["what time is it", "current time"]), MODULE, system_time)
    registry.register("stopwatch_start", aliases(["запусти секундомер", "старт секундомер", "начни отсчёт", "секундомер старт", "тайминг старт", "run stopwatch", "засеки время"], ["start stopwatch", "begin stopwatch"]), MODULE, stopwatch)
    registry.register("stopwatch_stop", aliases(["останови секундомер", "стоп секундомер", "заверши отсчёт", "покажи секундомер", "секундомер стоп", "stop stopwatch", "закончить тайминг"], ["stop stopwatch", "end stopwatch"]), MODULE, stopwatch_stop)
    registry.register("social_x", aliases(["открой x", "открой twitter", "твиттер", "соцсеть x", "лента x", "перейди в x", "икс соцсеть"], ["open x", "open twitter"]), MODULE, lambda **k: act.open_url("https://x.com"))
    registry.register("social_linkedin", aliases(["открой linkedin", "линкедин", "проф сеть", "linkedin профиль", "лента linkedin", "перейди в linkedin", "линкед ин"], ["open linkedin", "linkedin feed"]), MODULE, lambda **k: act.open_url("https://www.linkedin.com"))
    registry.register("social_instagram", aliases(["открой инстаграм", "инстаграм", "instagram", "лента инсты", "перейди в инсту", "соцсеть инста", "instagram open"], ["open instagram", "instagram feed"]), MODULE, lambda **k: act.open_url("https://www.instagram.com"))
    registry.register("social_facebook", aliases(["открой фейсбук", "facebook", "лента фейсбук", "соцсеть fb", "перейди в facebook", "фб", "facebook open"], ["open facebook", "facebook feed"]), MODULE, lambda **k: act.open_url("https://www.facebook.com"))
