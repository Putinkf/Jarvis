from __future__ import annotations

import os
from pathlib import Path

from jarvis.modules import base_actions as act
from jarvis.utils.logging_utils import action_guard

MODULE = "System & Hardware"


def aliases(ru: list[str], en: list[str]) -> list[str]:
    return ru + en


@action_guard(MODULE)
def open_task_manager(*, core, transcript: str) -> None:
    act.hotkey("ctrl", "shift", "esc")
    core.speak("Открываю диспетчер задач, сэр.")


@action_guard(MODULE)
def lock_pc(*, core, transcript: str) -> None:
    act.lock_screen()
    core.speak("Блокирую рабочую станцию, сэр.")


@action_guard(MODULE)
def clean_trash(*, core, transcript: str) -> None:
    os.system("powershell -Command Clear-RecycleBin -Force")
    core.speak("Корзина очищена, сэр.")


@action_guard(MODULE)
def launch_notepad(*, core, transcript: str) -> None:
    act.launch("notepad")
    core.speak("Открываю блокнот, сэр.")


@action_guard(MODULE)
def report_health(*, core, transcript: str) -> None:
    core.speak(f"Сэр, {act.cpu_ram_report()} {act.battery_report()}")


@action_guard(MODULE)
def shutdown_pc(*, core, transcript: str) -> None:
    if core.confirm("Подтвердите выключение"):
        os.system("shutdown /s /t 10")
        core.speak("Выключение через 10 секунд, сэр.")


@action_guard(MODULE)
def restart_pc(*, core, transcript: str) -> None:
    if core.confirm("Подтвердите перезагрузку"):
        os.system("shutdown /r /t 10")
        core.speak("Перезагрузка через 10 секунд, сэр.")


@action_guard(MODULE)
def sleep_pc(*, core, transcript: str) -> None:
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    core.speak("Перевожу систему в сон, сэр.")


@action_guard(MODULE)
def sort_downloads(*, core, transcript: str) -> None:
    down = Path.home() / "Downloads"
    for item in down.glob("*"):
        if item.is_dir():
            continue
        ext = item.suffix.replace(".", "").lower() or "other"
        target = down / ext
        target.mkdir(exist_ok=True)
        item.rename(target / item.name)
    core.speak("Папка загрузок отсортирована, сэр.")


def register(registry) -> None:
    registry.register("task_manager", aliases(["открой диспетчер задач", "диспетчер задач", "покажи процессы", "монитор ресурсов", "управление задачами", "task manager открой", "процессы windows"], ["open task manager", "task manager"]), MODULE, open_task_manager)
    registry.register("lock_pc", aliases(["заблокируй экран", "блокировка компьютера", "заблокируй пк", "замок экран", "lock windows", "сделай блокировку", "блок экрана"], ["lock screen", "lock computer"]), MODULE, lock_pc)
    registry.register("clean_trash", aliases(["очисти корзину", "удали мусор", "пустая корзина", "очистка корзины", "сотри корзину", "clear recycle bin", "убери мусор"], ["clean recycle bin", "empty trash"]), MODULE, clean_trash)
    registry.register("launch_notepad", aliases(["открой блокнот", "запусти блокнот", "создай текстовый файл", "нотпад", "заметки открой", "блокнот", "new note"], ["open notepad", "start notepad"]), MODULE, launch_notepad)
    registry.register("health_report", aliases(["отчет о системе", "здоровье системы", "нагрузка процессора", "статус железа", "состояние батареи", "проверка ресурсов", "системный отчет"], ["system health", "health report"]), MODULE, report_health)
    registry.register("shutdown", aliases(["выключи компьютер", "заверши работу", "выключение пк", "отключи систему", "power off", "пора выключаться", "выруби компьютер"], ["shutdown pc", "turn off computer"]), MODULE, shutdown_pc)
    registry.register("restart", aliases(["перезагрузи компьютер", "перезапуск системы", "сделай ребут", "рестарт windows", "reboot", "перезагрузка пк", "перезапусти"], ["restart pc", "reboot computer"]), MODULE, restart_pc)
    registry.register("sleep", aliases(["режим сна", "усыпи компьютер", "сон пк", "спящий режим", "suspend system", "усыпить систему", "пауза питания"], ["sleep pc", "hibernate system"]), MODULE, sleep_pc)
    registry.register("sort_downloads", aliases(["отсортируй загрузки", "разложи файлы", "организуй загрузки", "папку загрузок в порядок", "автосортировка", "сортировка download", "прибери загрузки"], ["sort downloads", "organize downloads"]), MODULE, sort_downloads)

    registry.register("snap_left", aliases(["окно влево", "прижми окно влево", "левая половина", "размести слева", "snap left", "окно налево", "влево экран"], ["snap window left", "move window left"]), MODULE, lambda **k: act.hotkey("win", "left"))
    registry.register("snap_right", aliases(["окно вправо", "прижми окно вправо", "правая половина", "размести справа", "snap right", "окно направо", "вправо экран"], ["snap window right", "move window right"]), MODULE, lambda **k: act.hotkey("win", "right"))
    registry.register("snap_up", aliases(["разверни окно", "максимизируй", "на весь экран", "окно вверх", "snap up", "увеличь окно", "полный экран"], ["maximize window", "window full screen"]), MODULE, lambda **k: act.hotkey("win", "up"))
    registry.register("snap_down", aliases(["сверни окно", "уменьши окно", "окно вниз", "минимизируй", "snap down", "убери окно", "свернуть"], ["minimize window", "window minimize"]), MODULE, lambda **k: act.hotkey("win", "down"))
    registry.register("open_explorer", aliases(["открой проводник", "проводник", "файлы windows", "менеджер файлов", "this pc", "открой папки", "explorer"], ["open explorer", "open files"]), MODULE, lambda **k: act.launch("explorer"))
    registry.register("open_settings", aliases(["открой настройки", "настройки windows", "параметры системы", "меню настроек", "settings open", "конфигурация", "параметры"], ["open settings", "system settings"]), MODULE, lambda **k: act.hotkey("win", "i"))
    registry.register("open_run", aliases(["открой выполнить", "окно выполнить", "run dialog", "команда выполнить", "win r", "запуск команды", "выполнить"], ["open run", "run dialog"]), MODULE, lambda **k: act.hotkey("win", "r"))
    registry.register("show_desktop", aliases(["покажи рабочий стол", "сверни все окна", "рабочий стол", "desktop show", "на стол", "скрыть окна", "открыть стол"], ["show desktop", "minimize all"]), MODULE, lambda **k: act.hotkey("win", "d"))
    registry.register("search_files", aliases(["поиск файлов", "найди файл", "поиск на компьютере", "ищи документ", "file search", "поиск windows", "найти документ"], ["search files", "locate file"]), MODULE, lambda **k: act.hotkey("win", "s"))
    registry.register("volume_up", aliases(["сделай громче", "громкость вверх", "увеличь звук", "добавь громкость", "volume up", "звук плюс", "громче"], ["volume up", "increase volume"]), MODULE, lambda **k: act.press("volumeup"))
    registry.register("volume_down", aliases(["сделай тише", "громкость вниз", "уменьши звук", "убавь громкость", "volume down", "звук минус", "тише"], ["volume down", "decrease volume"]), MODULE, lambda **k: act.press("volumedown"))
    registry.register("mute", aliases(["выключи звук", "без звука", "mute", "тишина", "приглуши звук", "звук выкл", "мьют"], ["mute volume", "silence audio"]), MODULE, lambda **k: act.press("volumemute"))
    registry.register("open_calculator", aliases(["открой калькулятор", "запусти калькулятор", "calc", "калькулятор", "посчитать", "кальк", "быстрый расчет"], ["open calculator", "launch calculator"]), MODULE, lambda **k: act.launch("calc"))
    registry.register("open_cmd", aliases(["открой командную строку", "запусти cmd", "консоль", "терминал windows", "command prompt", "cmd открой", "командная строка"], ["open command prompt", "launch cmd"]), MODULE, lambda **k: act.launch("start cmd"))
    registry.register("open_powershell", aliases(["открой powershell", "запусти павершел", "powershell", "виндовс оболочка", "консоль powershell", "силовая оболочка", "павершел"], ["open powershell", "launch powershell"]), MODULE, lambda **k: act.launch("start powershell"))
