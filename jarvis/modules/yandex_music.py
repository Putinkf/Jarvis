from __future__ import annotations

from jarvis.modules import base_actions as act
from jarvis.utils.logging_utils import action_guard

MODULE = "Yandex Music"


codex/create-modular-voice-assistant-jarvis-0b32yk
def aliases(ru: list[str], en: list[str]) -> list[str]:
    return ru + en


@action_guard(MODULE)
def play_pause(*, core, transcript: str) -> None:
    act.press("playpause")
    core.speak("Переключаю воспроизведение, сэр.")


@action_guard(MODULE)
def next_track(*, core, transcript: str) -> None:
    act.press("nexttrack")
codex/create-modular-voice-assistant-jarvis-0b32yk
    core.speak("Включаю следующий трек, сэр.")



@action_guard(MODULE)
def prev_track(*, core, transcript: str) -> None:
    act.press("prevtrack")
codex/create-modular-voice-assistant-jarvis-0b32yk
    core.speak("Возвращаю предыдущий трек, сэр.")



@action_guard(MODULE)
def like_track(*, core, transcript: str) -> None:
    act.press("l")
codex/create-modular-voice-assistant-jarvis-0b32yk
    core.speak("Ставлю лайк композиции, сэр.")



@action_guard(MODULE)
def search_track(*, core, transcript: str) -> None:
codex/create-modular-voice-assistant-jarvis-0b32yk
    query = (
        transcript.lower()
        .replace("найди", "")
        .replace("поиск", "")
        .replace("search", "")
        .replace("find", "")
        .strip()
        or "lofi"
    )
    act.hotkey("ctrl", "l")
    act.typewrite(query)
    act.press("enter")
    core.speak(f"Запускаю поиск: {query}, сэр.")


@action_guard(MODULE)
def open_daily_mix(*, core, transcript: str) -> None:
    act.open_url("https://music.yandex.ru/home")
codex/create-modular-voice-assistant-jarvis-0b32yk
    core.speak("Открываю ваш Daily Mix, сэр.")


def register(registry) -> None:
    registry.register(
        "music_play_pause",
        aliases(
            [
                "включи музыку",
                "пауза музыка",
                "поставь музыку на паузу",
                "продолжи музыку",
                "старт музыка",
                "музыка стоп",
                "плей пауза",
            ],
            ["play music", "pause music", "toggle music", "media play pause"],
        ),
        MODULE,
        play_pause,
    )
    registry.register(
        "music_next",
        aliases(
            ["следующий трек", "пропусти песню", "дальше", "вперёд трек", "следующая песня", "скип трек", "включи следующий"],
            ["next track", "skip song", "play next"],
        ),
        MODULE,
        next_track,
    )
    registry.register(
        "music_prev",
        aliases(
            ["предыдущий трек", "назад песня", "верни трек", "прошлая песня", "включи прошлый", "верни назад", "предыдущая композиция"],
            ["previous track", "last song", "go back song"],
        ),
        MODULE,
        prev_track,
    )
    registry.register(
        "music_like",
        aliases(
            ["лайк трек", "поставь лайк", "мне нравится", "добавь в любимое", "нравится песня", "оценка нравится", "лайкни"],
            ["like this song", "like track", "mark favorite"],
        ),
        MODULE,
        like_track,
    )
    registry.register(
        "music_search",
        aliases(
            ["найди трек", "поиск песни", "найди исполнителя", "ищи музыку", "поиск в яндекс музыке", "включи песню", "найти композицию"],
            ["search song", "find track", "search in yandex music", "find artist"],
        ),
        MODULE,
        search_track,
    )
    registry.register(
        "music_daily_mix",
        aliases(
            ["открой дэйли микс", "открой ежедневный микс", "мой микс дня", "запусти daily mix", "плейлист дня", "включи микс", "дневной плейлист"],
            ["open daily mix", "start my mix", "open playlist daily mix"],
        ),
        MODULE,
        open_daily_mix,
    )
