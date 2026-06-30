from actions.apps import open_vscode, open_notepad, open_calculator, open_chrome
from actions.browser import google_search, open_google
from actions.init_setup import initialize_setup

# Signal returned when query needs LLM (not a command)
NEEDS_LLM = "__LLM__"


def route_command(text):
    t = text.lower()

    if any(x in t for x in ["initialize my setup", "initialize setup"]):
        return initialize_setup()

    if any(x in t for x in ["open vs code", "open visual studio"]):
        return open_vscode()

    if "open notepad" in t:
        return open_notepad()

    if "open calculator" in t:
        return open_calculator()

    if "open chrome" in t:
        return open_chrome()

    if "open google" in t:
        return open_google()

    if "search" in t and "google" in t:
        query = (t.replace("search", "")
                  .replace("on google", "")
                  .replace("google", "")
                  .strip())
        return google_search(query)

    return NEEDS_LLM