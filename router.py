from actions.apps import open_vscode, open_notepad, open_calculator, open_chrome
from actions.browser import google_search, open_google
from actions.init_setup import initialize_setup
from llm import ask_friday


def route_command(text):
    text_lower = text.lower()

    # --- Setup routine ---
    if "initialize my setup" in text_lower or "initialize setup" in text_lower:
        return initialize_setup()

    # --- App opening ---
    if "open vs code" in text_lower or "open visual studio" in text_lower:
        return open_vscode()

    if "open notepad" in text_lower:
        return open_notepad()

    if "open calculator" in text_lower:
        return open_calculator()

    if "open chrome" in text_lower:
        return open_chrome()

    if "open google" in text_lower:
        return open_google()

    # --- Google search ---
    if "search" in text_lower and "google" in text_lower:
        query = text_lower.replace("search", "").replace("on google", "").replace("google", "").strip()
        return google_search(query)

    # --- Nothing matched, send to LLM for normal conversation ---
    return ask_friday(text)