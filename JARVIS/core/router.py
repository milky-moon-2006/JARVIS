import re

from core.security import confirm_action
from skills.windows import (
    open_app,
    lock,
    shutdown,
    restart,
    cancel_shutdown,
)
from skills.web import (
    open_site,
    google_search,
    youtube_search,
)
from skills.whatsapp import send_whatsapp
from skills.vision import open_camera


def handle(command):
    c = command.strip().lower()

    # ==============================
    # WEBSITES
    # ==============================

    if c.startswith("open "):
        name = c[5:].strip()

        if open_site(name):
            return f"Opening {name}."

    # ==============================
    # WINDOWS APPLICATIONS
    # ==============================

    apps = {
        "open chrome": "chrome",
        "open edge": "edge",
        "open notepad": "notepad",
        "open calculator": "calculator",
        "open calc": "calc",
        "open explorer": "explorer",
        "open file explorer": "file explorer",
        "open vscode": "vscode",
        "open vs code": "vs code",
    }

    if c in apps:
        if open_app(apps[c]):
            return "Opening application."

        return "I could not open that application."

    # ==============================
    # GOOGLE SEARCH
    # ==============================

    if c.startswith("search google for "):
        query = c[len("search google for "):].strip()

        google_search(query)

        return "Google search opened."

    # ==============================
    # YOUTUBE SEARCH
    # ==============================

    if c.startswith("search youtube for "):
        query = c[len("search youtube for "):].strip()

        youtube_search(query)

        return "YouTube search opened."

    # ==============================
    # LOCK COMPUTER
    # ==============================

    if c in {
        "lock laptop",
        "lock my laptop",
        "lock computer",
    }:
        lock()

        return "Computer locked."

    # ==============================
    # CANCEL SHUTDOWN
    # ==============================

    if c in {
        "cancel shutdown",
        "abort shutdown",
    }:
        cancel_shutdown()

        return "Pending shutdown cancelled."

    # ==============================
    # SHUTDOWN
    # ==============================

    if c in {
        "shutdown laptop",
        "shutdown my laptop",
        "shutdown computer",
        "turn off my laptop",
    }:

        confirmed = confirm_action(
            "Shutdown requested.",
            "Windows will shut down in 10 seconds.",
        )

        if confirmed:
            shutdown()

            return "Shutdown command accepted."

        return "Shutdown cancelled."

    # ==============================
    # RESTART
    # ==============================

    if c in {
        "restart laptop",
        "restart my laptop",
        "restart computer",
    }:

        confirmed = confirm_action(
            "Restart requested.",
            "Windows will restart in 10 seconds.",
        )

        if confirmed:
            restart()

            return "Restart command accepted."

        return "Restart cancelled."

    # ==============================
    # WHATSAPP
    # ==============================

    match = re.match(
        r"send whatsapp to (.+?) saying (.+)",
        c,
    )

    if match:

        contact, message = match.groups()

        confirmed = confirm_action(
            "WhatsApp message requested.",
            f"Contact: {contact}\nMessage: {message}",
        )

        if confirmed:

            success = send_whatsapp(
                contact,
                message,
            )

            if success:
                return "WhatsApp message sent."

            return "I could not send the WhatsApp message."

        return "WhatsApp message cancelled."

    # ==============================
    # CAMERA
    # ==============================

    if c in {
        "open camera",
        "start camera",
        "camera",
    }:
        return open_camera()

    # ==============================
    # SEND UNKNOWN COMMAND TO AI
    # ==============================

    return None