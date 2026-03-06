from __future__ import annotations

import os
from pathlib import Path

from jarvis.modules import base_actions as act
from jarvis.utils.logging_utils import action_guard

MODULE = "System & Hardware"


@action_guard(MODULE)
def open_task_manager(*, core, transcript: str) -> None:
    act.hotkey("ctrl", "shift", "esc")
    core.speak("Opening task manager.")


@action_guard(MODULE)
def lock_pc(*, core, transcript: str) -> None:
    act.lock_screen()


@action_guard(MODULE)
def clean_trash(*, core, transcript: str) -> None:
    os.system("powershell -Command Clear-RecycleBin -Force")
    core.speak("Recycle bin cleaned.")


@action_guard(MODULE)
def launch_notepad(*, core, transcript: str) -> None:
    act.launch("notepad")
    core.speak("Notepad launched.")


@action_guard(MODULE)
def report_health(*, core, transcript: str) -> None:
    core.speak(f"{act.cpu_ram_report()} {act.battery_report()}")


@action_guard(MODULE)
def shutdown_pc(*, core, transcript: str) -> None:
    if core.confirm("Confirm shutdown"):
        os.system("shutdown /s /t 10")
        core.speak("Shutdown in 10 seconds.")


@action_guard(MODULE)
def restart_pc(*, core, transcript: str) -> None:
    if core.confirm("Confirm restart"):
        os.system("shutdown /r /t 10")
        core.speak("Restart in 10 seconds.")


@action_guard(MODULE)
def sleep_pc(*, core, transcript: str) -> None:
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


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
    core.speak("Downloads organized.")


def register(registry) -> None:
    registry.register("task_manager", ["open task manager", "task manager", "show processes", "performance manager", "system monitor open"], MODULE, open_task_manager)
    registry.register("lock_pc", ["lock screen", "lock computer", "secure workstation", "windows lock", "screen lock now"], MODULE, lock_pc)
    registry.register("clean_trash", ["clean recycle bin", "empty trash", "clear bin", "trash cleaner", "delete recycle bin items"], MODULE, clean_trash)
    registry.register("launch_notepad", ["open notepad", "start notepad", "create text file", "launch notes", "quick note app"], MODULE, launch_notepad)
    registry.register("health_report", ["system health", "health report", "cpu ram status", "hardware status", "battery and cpu"], MODULE, report_health)
    registry.register("shutdown", ["shutdown pc", "turn off computer", "power off windows", "shutdown system", "switch off machine"], MODULE, shutdown_pc)
    registry.register("restart", ["restart pc", "reboot computer", "restart windows", "system reboot", "reload machine"], MODULE, restart_pc)
    registry.register("sleep", ["sleep pc", "sleep computer", "hibernate system", "standby mode", "put system to sleep"], MODULE, sleep_pc)
    registry.register("sort_downloads", ["sort downloads", "organize downloads", "auto sort files", "clean download folder", "arrange downloaded files"], MODULE, sort_downloads)

    registry.register("snap_left", ["snap window left", "move window left", "dock left", "window left half", "split window left"], MODULE, lambda **k: act.hotkey("win", "left"))
    registry.register("snap_right", ["snap window right", "move window right", "dock right", "window right half", "split window right"], MODULE, lambda **k: act.hotkey("win", "right"))
    registry.register("snap_up", ["maximize window", "snap up", "window full screen", "expand window", "move window top"], MODULE, lambda **k: act.hotkey("win", "up"))
    registry.register("snap_down", ["minimize window", "snap down", "window minimize", "collapse window", "move window bottom"], MODULE, lambda **k: act.hotkey("win", "down"))
    registry.register("open_explorer", ["open explorer", "open files", "file manager", "show folders", "open this pc"], MODULE, lambda **k: act.launch("explorer"))
    registry.register("open_settings", ["open settings", "windows settings", "system settings", "launch settings", "configure windows"], MODULE, lambda **k: act.hotkey("win", "i"))
    registry.register("open_run", ["open run", "run dialog", "show run box", "launch run window", "quick run"], MODULE, lambda **k: act.hotkey("win", "r"))
    registry.register("show_desktop", ["show desktop", "hide all windows", "desktop view", "minimize all", "display desktop"], MODULE, lambda **k: act.hotkey("win", "d"))
    registry.register("search_files", ["search files", "find document", "locate file", "file search", "search on computer"], MODULE, lambda **k: act.hotkey("win", "s"))
    registry.register("wifi_toggle", ["toggle wifi", "wifi on", "wifi off", "switch wireless", "internet adapter toggle"], MODULE, lambda **k: act.hotkey("fn", "f2"))
    registry.register("camera_toggle", ["toggle camera", "camera on", "camera off", "disable webcam", "enable webcam"], MODULE, lambda **k: act.hotkey("fn", "f8"))
    registry.register("volume_up", ["volume up", "increase volume", "louder", "sound up", "raise audio"], MODULE, lambda **k: act.press("volumeup"))
    registry.register("volume_down", ["volume down", "decrease volume", "quieter", "sound down", "lower audio"], MODULE, lambda **k: act.press("volumedown"))
    registry.register("mute", ["mute volume", "silence audio", "toggle mute", "mute sound", "quiet mode"], MODULE, lambda **k: act.press("volumemute"))
    registry.register("brightness_up", ["brightness up", "increase brightness", "screen brighter", "light up display", "raise brightness"], MODULE, lambda **k: act.hotkey("fn", "f6"))
    registry.register("brightness_down", ["brightness down", "decrease brightness", "dim screen", "reduce display light", "lower brightness"], MODULE, lambda **k: act.hotkey("fn", "f5"))

    extra = [
        ("open_start", ["open start menu", "start menu", "windows start", "launch start", "show start"], lambda **k: act.press("win")),
        ("open_notifications", ["open notifications", "notification center", "show notifications", "windows notifications", "alerts panel"], lambda **k: act.hotkey("win", "a")),
        ("open_action_center", ["open action center", "quick settings", "control center", "windows quick panel", "toggle action center"], lambda **k: act.hotkey("win", "a")),
        ("open_clipboard", ["open clipboard", "clipboard history", "show clipboard", "paste history", "windows clipboard"], lambda **k: act.hotkey("win", "v")),
        ("open_emoji", ["emoji panel", "open emoji", "windows emoji", "insert emoji", "emoji keyboard"], lambda **k: act.hotkey("win", ".")),
        ("screenshot_area", ["take screenshot", "screen snip", "capture area", "snipping tool", "quick screenshot"], lambda **k: act.hotkey("win", "shift", "s")),
        ("new_virtual_desktop", ["new desktop", "create virtual desktop", "add desktop", "virtual desktop new", "another desktop"], lambda **k: act.hotkey("win", "ctrl", "d")),
        ("close_virtual_desktop", ["close desktop", "remove virtual desktop", "delete desktop", "virtual desktop close", "end desktop"], lambda **k: act.hotkey("win", "ctrl", "f4")),
        ("desktop_left", ["desktop left", "switch desktop left", "previous desktop", "move desktop left", "virtual desktop back"], lambda **k: act.hotkey("win", "ctrl", "left")),
        ("desktop_right", ["desktop right", "switch desktop right", "next desktop", "move desktop right", "virtual desktop next"], lambda **k: act.hotkey("win", "ctrl", "right")),
        ("alt_tab", ["switch window", "next window", "alt tab", "change app", "window switcher"], lambda **k: act.hotkey("alt", "tab")),
        ("close_window", ["close window", "exit window", "terminate current app", "quit window", "close app"], lambda **k: act.hotkey("alt", "f4")),
        ("rename_file", ["rename file", "change file name", "quick rename", "rename selected", "file rename"], lambda **k: act.press("f2")),
        ("delete_file", ["delete file", "remove selected file", "trash selected", "delete selected", "erase file"], lambda **k: act.press("delete")),
        ("permanent_delete", ["permanent delete", "delete forever", "shift delete", "hard delete", "remove permanently"], lambda **k: act.hotkey("shift", "delete")),
        ("copy", ["copy", "copy item", "copy selected", "duplicate selection", "copy now"], lambda **k: act.hotkey("ctrl", "c")),
        ("paste", ["paste", "paste item", "insert clipboard", "paste now", "apply paste"], lambda **k: act.hotkey("ctrl", "v")),
        ("cut", ["cut", "cut item", "move selection", "cut selected", "remove and copy"], lambda **k: act.hotkey("ctrl", "x")),
        ("undo", ["undo", "revert action", "step back", "undo command", "rollback"], lambda **k: act.hotkey("ctrl", "z")),
        ("redo", ["redo", "repeat action", "step forward", "redo command", "apply again"], lambda **k: act.hotkey("ctrl", "y")),
        ("select_all", ["select all", "highlight all", "mark everything", "select everything", "all selection"], lambda **k: act.hotkey("ctrl", "a")),
        ("save", ["save file", "save this", "quick save", "store file", "write changes"], lambda **k: act.hotkey("ctrl", "s")),
        ("find", ["find text", "search in page", "find item", "open find", "locate text"], lambda **k: act.hotkey("ctrl", "f")),
        ("print", ["print document", "send to printer", "start printing", "hard copy", "print this"], lambda **k: act.hotkey("ctrl", "p")),
        ("zoom_in", ["zoom in", "increase zoom", "make bigger", "enlarge view", "magnify"], lambda **k: act.hotkey("ctrl", "+")),
        ("zoom_out", ["zoom out", "decrease zoom", "make smaller", "reduce view", "minify"], lambda **k: act.hotkey("ctrl", "-")),
        ("open_cmd", ["open command prompt", "launch cmd", "terminal cmd", "command line", "open console"], lambda **k: act.launch("start cmd")),
        ("open_powershell", ["open powershell", "launch powershell", "windows terminal", "open shell", "admin shell"], lambda **k: act.launch("start powershell")),
        ("open_control_panel", ["open control panel", "control panel", "legacy settings", "windows control", "open cp"], lambda **k: act.launch("control")),
        ("open_device_manager", ["open device manager", "device manager", "hardware devices", "manage devices", "drivers panel"], lambda **k: act.launch("devmgmt.msc")),
        ("open_disk_cleanup", ["open disk cleanup", "disk cleanup", "clean disk", "temporary files cleanup", "storage cleanup"], lambda **k: act.launch("cleanmgr")),
        ("open_services", ["open services", "services manager", "windows services", "background services", "service console"], lambda **k: act.launch("services.msc")),
        ("open_registry_editor", ["open registry", "registry editor", "regedit", "windows registry", "edit registry"], lambda **k: act.launch("regedit")),
        ("open_system_info", ["system information", "open msinfo", "hardware summary", "pc information", "system specs"], lambda **k: act.launch("msinfo32")),
        ("open_resource_monitor", ["open resource monitor", "resource monitor", "performance details", "cpu monitor", "resource usage"], lambda **k: act.launch("resmon")),
        ("open_event_viewer", ["open event viewer", "system logs", "view events", "windows logs", "event logs"], lambda **k: act.launch("eventvwr")),
        ("network_connections", ["open network connections", "network adapters", "internet connections", "manage network", "adapter settings"], lambda **k: act.launch("ncpa.cpl")),
        ("bluetooth_settings", ["open bluetooth", "bluetooth settings", "pair device", "wireless devices", "bluetooth panel"], lambda **k: act.hotkey("win", "i")),
        ("open_calculator", ["open calculator", "launch calculator", "calculator app", "start calc", "quick calc"], lambda **k: act.launch("calc")),
        ("open_paint", ["open paint", "launch paint", "draw app", "mspaint", "paint program"], lambda **k: act.launch("mspaint")),
        ("open_camera", ["open camera", "launch camera app", "take photo app", "camera application", "start webcam app"], lambda **k: act.launch("start microsoft.windows.camera:")),
        ("open_snipping_tool", ["open snipping tool", "launch snipping", "screen capture tool", "snip tool", "snipping app"], lambda **k: act.launch("snippingtool")),
    ]
    for name, aliases, handler in extra:
        registry.register(name, aliases, MODULE, handler)
