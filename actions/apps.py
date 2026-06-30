import subprocess

def open_vscode():
    subprocess.Popen("code", shell=True)
    return "VS Code opened successfully"


def open_notepad():
    subprocess.Popen("notepad", shell=True)
    return "Notepad opened successfully"


def open_calculator():
    subprocess.Popen("calc", shell=True)
    return "Calculator opened successfully"

def open_chrome():
    subprocess.Popen("start chrome", shell=True)
    return "Chrome opened successfully"