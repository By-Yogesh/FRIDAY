import subprocess

def open_vscode():
    subprocess.Popen("code", shell=True)
    return "Opening VS Code"


def open_notepad():
    subprocess.Popen("notepad", shell=True)
    return "Opening Notepad"


def open_calculator():
    subprocess.Popen("calc", shell=True)
    return "Opening Calculator"

def open_chrome():
    subprocess.Popen("start chrome", shell=True)
    return "Opening Chrome"