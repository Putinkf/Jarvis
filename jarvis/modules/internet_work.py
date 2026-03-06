from __future__ import annotations

import smtplib
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

import pandas as pd
from docx import Document

from jarvis.modules import base_actions as act
from jarvis.utils.logging_utils import action_guard

MODULE = "Internet & Work"


@action_guard(MODULE)
def google_search(*, core, transcript: str) -> None:
    q = transcript.replace("search", "").replace("google", "").strip() or "python"
    act.open_url(f"https://www.google.com/search?q={q.replace(' ', '+')}")
    core.speak(f"Searching Google for {q}.")


@action_guard(MODULE)
def wiki_search(*, core, transcript: str) -> None:
    q = transcript.replace("wikipedia", "").replace("wiki", "").strip() or "artificial intelligence"
    act.open_url(f"https://en.wikipedia.org/wiki/Special:Search?search={q.replace(' ', '+')}")


@action_guard(MODULE)
def youtube_search(*, core, transcript: str) -> None:
    q = transcript.replace("youtube", "").replace("search", "").strip() or "lofi"
    act.open_url(f"https://www.youtube.com/results?search_query={q.replace(' ', '+')}")


@action_guard(MODULE)
def create_docx(*, core, transcript: str) -> None:
    target = Path.home() / "Documents" / f"jarvis_{datetime.now():%Y%m%d_%H%M%S}.docx"
    doc = Document()
    doc.add_heading("JARVIS Document", level=1)
    doc.add_paragraph("Created by voice command.")
    doc.save(target)
    core.speak(f"Document created {target.name}.")


@action_guard(MODULE)
def create_xlsx(*, core, transcript: str) -> None:
    target = Path.home() / "Documents" / f"jarvis_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
    pd.DataFrame([{"task": "created by jarvis", "time": datetime.now().isoformat()}]).to_excel(target, index=False)
    core.speak(f"Spreadsheet created {target.name}.")


@action_guard(MODULE)
def send_email(*, core, transcript: str) -> None:
    sender = core.config.get("smtp_sender")
    password = core.config.get("smtp_password")
    recipient = core.config.get("smtp_recipient")
    server = core.config.get("smtp_server", "smtp.gmail.com")
    if not all([sender, password, recipient]):
        core.speak("SMTP config missing.")
        return
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = "JARVIS automated message"
    msg.set_content("Message sent from JARVIS voice command.")
    with smtplib.SMTP_SSL(server, 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
    core.speak("Email sent.")


def register(registry) -> None:
    registry.register("google", ["google search", "search google", "find on google", "google it", "web search"], MODULE, google_search)
    registry.register("wiki", ["search wikipedia", "wiki search", "find in wiki", "open wikipedia", "wikipedia lookup"], MODULE, wiki_search)
    registry.register("youtube", ["search youtube", "find video", "open youtube search", "youtube lookup", "play on youtube"], MODULE, youtube_search)
    registry.register("close_tab", ["close tab", "close browser tab", "remove tab", "dismiss tab", "exit tab"], MODULE, lambda **k: act.hotkey("ctrl", "w"))
    registry.register("history", ["open history", "browser history", "show browsing history", "history page", "view history"], MODULE, lambda **k: act.hotkey("ctrl", "h"))
    registry.register("incognito", ["open incognito", "private tab", "new incognito window", "private browsing", "secret mode"], MODULE, lambda **k: act.hotkey("ctrl", "shift", "n"))
    registry.register("new_tab", ["new tab", "open new tab", "create tab", "spawn tab", "browser new page"], MODULE, lambda **k: act.hotkey("ctrl", "t"))
    registry.register("refresh", ["refresh page", "reload page", "refresh tab", "update webpage", "page reload"], MODULE, lambda **k: act.press("f5"))
    registry.register("address_bar", ["focus address bar", "go to address bar", "url bar", "select address", "browser url input"], MODULE, lambda **k: act.hotkey("ctrl", "l"))
    registry.register("create_doc", ["create document", "new docx", "make word file", "create word doc", "draft document"], MODULE, create_docx)
    registry.register("create_sheet", ["create spreadsheet", "new excel", "make xlsx", "create workbook", "draft spreadsheet"], MODULE, create_xlsx)
    registry.register("send_email", ["send email", "email now", "compose and send mail", "dispatch email", "mail message"], MODULE, send_email)
    registry.register("calendar", ["open calendar", "create calendar event", "schedule meeting", "plan reminder", "manage calendar"], MODULE, lambda **k: act.open_url("https://calendar.google.com"))
    registry.register("telegram", ["send telegram message", "telegram automation", "telegram quick message", "message on telegram", "open telegram"], MODULE, lambda **k: act.launch("start telegram"))
    registry.register("discord", ["send discord message", "discord automation", "message on discord", "open discord", "discord quick message"], MODULE, lambda **k: act.launch("start discord"))
    registry.register("open_github", ["open github", "github website", "go to github", "launch github", "github home"], MODULE, lambda **k: act.open_url("https://github.com"))
    registry.register("open_stackoverflow", ["open stackoverflow", "developer q and a", "search stack overflow", "go stackoverflow", "coding help site"], MODULE, lambda **k: act.open_url("https://stackoverflow.com"))
    registry.register("news_tech", ["open tech news", "technology headlines", "latest tech news", "developer news", "hacker news"], MODULE, lambda **k: act.open_url("https://news.ycombinator.com"))
