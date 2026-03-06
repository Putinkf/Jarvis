from __future__ import annotations

import functools
import logging
from pathlib import Path
from typing import Any, Callable

LOG_FILE = Path("jarvis_log.txt")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger("jarvis")


def action_guard(module_name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator for logging actions and catching runtime errors."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                logger.info("[%s] Executing '%s'", module_name, func.__name__)
                return func(*args, **kwargs)
            except Exception as exc:  # noqa: BLE001 - controlled at boundary
                logger.exception("[%s] Failed '%s': %s", module_name, func.__name__, exc)
                core = kwargs.get("core")
                if core is not None:
                    core.speak(f"Сэр, доступ к модулю {module_name} ограничен. Проверяю систему...")
                return None

        return wrapper

    return decorator
