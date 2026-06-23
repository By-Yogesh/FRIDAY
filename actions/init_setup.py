import time
import webbrowser
from actions.apps import open_vscode

GITHUB_URL = "https://github.com/By-Yogesh"
LINKEDIN_URL = "https://linkedin.com/in/byyogesh"
INSTAGRAM_URL = "https://instagram.com/datawithyogesh"


def initialize_setup():

    webbrowser.open(GITHUB_URL)
    time.sleep(1)
    webbrowser.open(LINKEDIN_URL)
    time.sleep(1)
    webbrowser.open(INSTAGRAM_URL)

    open_vscode()
    time.sleep(1)  # small delay so apps don't clash while opening
    
    return "Your Setup is initialized. VS Code opened, GitHub opened in chrome, LinkedIn and Instagram are also opened."