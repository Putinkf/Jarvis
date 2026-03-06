from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Callable

try:
    from Levenshtein import ratio as levenshtein_ratio
except Exception:  # noqa: BLE001
    levenshtein_ratio = None


@dataclass(slots=True)
class CommandSpec:
    name: str
    aliases: list[str]
    handler: Callable[..., None]
    module: str


class CommandRegistry:
    def __init__(self, threshold: int = 70) -> None:
        self.threshold = threshold
        self._commands: dict[str, CommandSpec] = {}

    def register(self, name: str, aliases: list[str], module: str, handler: Callable[..., None]) -> None:
        self._commands[name] = CommandSpec(name=name, aliases=aliases, handler=handler, module=module)

    def all_commands(self) -> dict[str, CommandSpec]:
        return self._commands

    def _score(self, left: str, right: str) -> int:
        if levenshtein_ratio is not None:
            return int(levenshtein_ratio(left, right) * 100)
        return int(SequenceMatcher(None, left, right).ratio() * 100)

    def match(self, transcript: str) -> tuple[CommandSpec | None, int, str | None]:
        transcript = transcript.lower().strip()
        best_score = -1
        best_cmd: CommandSpec | None = None
        best_alias: str | None = None
        for cmd in self._commands.values():
            for alias in cmd.aliases:
                score = self._score(transcript, alias.lower())
                if score > best_score:
                    best_score, best_cmd, best_alias = score, cmd, alias

        if best_cmd is None or best_score < self.threshold:
            return None, best_score, best_alias
        return best_cmd, best_score, best_alias
