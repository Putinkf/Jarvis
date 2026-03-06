from __future__ import annotations

from jarvis.modules import base_actions as act
from jarvis.utils.logging_utils import action_guard

MODULE = "Yandex Music"


@action_guard(MODULE)
def play_pause(*, core, transcript: str) -> None:
    act.press("playpause")
    core.speak("Toggled playback.")


@action_guard(MODULE)
def next_track(*, core, transcript: str) -> None:
    act.press("nexttrack")
    core.speak("Next track.")


@action_guard(MODULE)
def prev_track(*, core, transcript: str) -> None:
    act.press("prevtrack")
    core.speak("Previous track.")


@action_guard(MODULE)
def like_track(*, core, transcript: str) -> None:
    act.press("l")
    core.speak("Track liked.")


@action_guard(MODULE)
def search_track(*, core, transcript: str) -> None:
    query = transcript.replace("search", "").replace("find", "").strip() or "lofi"
    act.hotkey("ctrl", "l")
    act.typewrite(query)
    act.press("enter")
    core.speak(f"Searching for {query}.")


@action_guard(MODULE)
def open_daily_mix(*, core, transcript: str) -> None:
    act.open_url("https://music.yandex.ru/home")
    core.speak("Opening Daily Mix.")


def register(registry) -> None:
    registry.register("music_play_pause", [
        "play music", "pause music", "toggle music", "music on", "music off", "media play pause"
    ], MODULE, play_pause)
    registry.register("music_next", [
        "next track", "skip song", "play next", "forward song", "next music"
    ], MODULE, next_track)
    registry.register("music_prev", [
        "previous track", "last song", "go back song", "rewind song", "previous music"
    ], MODULE, prev_track)
    registry.register("music_like", [
        "like this song", "like track", "thumbs up song", "mark favorite", "yandex like"
    ], MODULE, like_track)
    registry.register("music_search", [
        "search song", "find track", "search in yandex music", "find artist", "play song"
    ], MODULE, search_track)
    registry.register("music_daily_mix", [
        "open daily mix", "start my mix", "open playlist daily mix", "daily mix please"
    ], MODULE, open_daily_mix)
