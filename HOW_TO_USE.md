# 📖 HOW TO USE — FRIDAY AI Assistant

> Complete setup guide for running FRIDAY on any Windows machine from scratch.
> Follow every step in order. Don't skip anything.

---

## ✅ Before You Start — What You Need

Make sure your machine meets these basics:

- Windows 10 or Windows 11
- At least 8GB RAM
- At least 5GB free storage
- A working microphone
- Internet connection (only for setup — FRIDAY runs offline after)

---

## PART 1 — Download and Install Prerequisites

These are the core tools FRIDAY depends on. Install them in this order.

---

### Step 1 — Install Python 3.10+

FRIDAY is built in Python. You need Python 3.10 or higher.

**Download:** [https://www.python.org/downloads/](https://www.python.org/downloads/)

1. Click the yellow **"Download Python 3.x.x"** button
2. Run the installer
3. ⚠️ **IMPORTANT:** On the first screen of the installer, check the box that says **"Add Python to PATH"** before clicking Install Now
4. Click **"Install Now"**
5. Wait for it to finish, then click Close

**Verify it worked** — open Command Prompt and run:
```bash
python --version
```
You should see something like `Python 3.10.10`. If you see an error, Python was not added to PATH correctly — reinstall and make sure to check that box.

---

### Step 2 — Install Ollama

Ollama is what runs the Qwen AI model locally on your machine.

**Download:** [https://ollama.com/download](https://ollama.com/download)

1. Click **"Download for Windows"**
2. Run the `.exe` installer
3. Follow the installation steps (it's straightforward, just click Next)
4. Ollama will install and start running in the background

**Verify it worked** — open Command Prompt and run:
```bash
ollama --version
```
You should see a version number printed.

---

### Step 3 — Download the Qwen AI Model

This downloads the brain of FRIDAY — the language model that understands and replies to you.

Open Command Prompt and run:
```bash
ollama pull qwen2.5:3b
```

This is approximately **2GB** — it will take a few minutes depending on your internet speed. A progress bar will appear. Wait for it to finish completely before moving on.

**Verify it worked:**
```bash
ollama list
```
You should see `qwen2.5:3b` listed.

---

### Step 4 — Install Git (to clone the project)

Git lets you download the FRIDAY project code from GitHub.

**Download:** [https://git-scm.com/download/win](https://git-scm.com/download/win)

1. Click **"Click here to download"** for the latest version
2. Run the installer — keep all default settings, just click Next through everything
3. Click Install, then Finish

**Verify it worked:**
```bash
git --version
```
You should see something like `git version 2.x.x`.

---

## PART 2 — Get the FRIDAY Project

---

### Step 5 — Clone the Repository

Open Command Prompt and run these commands one by one:

```bash
# Go to the drive/folder where you want to install FRIDAY
cd C:\

# Clone the project (replace YOUR_USERNAME with the actual GitHub username)
git clone https://github.com/YOUR_USERNAME/FRIDAY.git

# Go into the project folder
cd FRIDAY
```

> If you don't want to use Git, you can also go to the GitHub page, click the green **"Code"** button → **"Download ZIP"**, extract it, and rename the folder to `FRIDAY`.

---

### Step 6 — Create a Virtual Environment

A virtual environment is a clean, isolated space for FRIDAY's Python packages. This prevents any conflicts with other Python projects on your machine.

Inside the `FRIDAY` folder, run:
```bash
python -m venv friday_env
```

Then activate it:
```bash
friday_env\Scripts\activate
```

You'll know it's active when your terminal line starts with `(friday_env)` like this:
```
(friday_env) C:\FRIDAY>
```

> ⚠️ You must activate the virtual environment **every time** you open a new Command Prompt to run FRIDAY. Just run `friday_env\Scripts\activate` again.

---

## PART 3 — Install Python Packages

Make sure your virtual environment is active (you see `(friday_env)` at the start of your terminal line) before running these.

Install each package one by one — do not paste all at once:

```bash
pip install --upgrade pip
```

```bash
pip install faster-whisper
```

```bash
pip install kokoro-onnx
```

```bash
pip install webrtcvad-wheels
```

```bash
pip install pyaudio
```

> If `pyaudio` fails, run these instead:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

```bash
pip install sounddevice
```

```bash
pip install soundfile
```

```bash
pip install keyboard
```

```bash
pip install ollama
```

```bash
pip install numpy
```

**Verify all packages are installed:**
```bash
pip list
```

You should see all of the above packages listed.

---

## PART 4 — Download Kokoro Voice Model Files

Kokoro is the voice of FRIDAY. It needs two model files that are too large to store on GitHub, so you download them separately.

**Download page:** [https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0)

Scroll down to the **Assets** section and download exactly these two files:

| File | Size | Notes |
|---|---|---|
| `kokoro-v1.0.int8.onnx` | ~88MB | ✅ Use this one (lightest, best for regular laptops) |
| `voices-v1.0.bin` | ~250MB | ✅ Required |

> ⚠️ Do NOT download `kokoro-v1.0.onnx` or `kokoro-v1.0.fp16.onnx` — those are larger and slower.

**After downloading:** Move both files directly into your `FRIDAY` folder so the structure looks like:

```
FRIDAY/
├── kokoro-v1.0.int8.onnx   ✅
├── voices-v1.0.bin          ✅
├── main.py
├── config.py
└── ...
```

---

## PART 5 — Configure FRIDAY For Your Machine

---

### Step 7 — Update Your Personal URLs in init_setup.py

FRIDAY's "initialize my setup" command opens your personal profile pages. You need to update these with your actual URLs.

Open `actions/init_setup.py` in any text editor (Notepad, VS Code, etc.) and find these lines:

```python
GITHUB_URL = "https://github.com/YOUR_USERNAME"
LINKEDIN_URL = "https://linkedin.com/in/YOUR_USERNAME"
INSTAGRAM_URL = "https://instagram.com/YOUR_USERNAME"
```

Replace `YOUR_USERNAME` in each line with your actual usernames for each platform. Save the file.

---

### Step 8 — (Optional) Change the Hotkey

The default hotkey to wake FRIDAY is `Ctrl+Alt+Space`.

If you want to change it, open `main.py` and find this line:
```python
keyboard.wait("ctrl+alt+space")
```
Change `"ctrl+alt+space"` to whatever combination you prefer, for example `"alt+space"` or `"ctrl+shift+f"`.

---

## PART 6 — Run FRIDAY

---

### Step 9 — Start Ollama (First Time or After Restart)

Ollama needs to be running in the background for FRIDAY's brain to work.

Open a **separate** Command Prompt window and run:
```bash
ollama serve
```

Keep this window open in the background. You don't need to touch it again.

> On most systems, Ollama starts automatically when Windows boots. You can check by running `ollama ps` — if it responds, it's already running and you don't need to run `ollama serve` manually.

---

### Step 10 — Run FRIDAY

Open a **new** Command Prompt window, navigate to your FRIDAY folder, activate the virtual environment, and start FRIDAY:

```bash
cd C:\FRIDAY
friday_env\Scripts\activate
python main.py
```

> ⚠️ Run CMD as **Administrator** for the hotkey to work across all apps:
> Right-click on Command Prompt → **Run as Administrator**, then run the commands above.

FRIDAY will load its models (takes about 10-20 seconds the first time), then greet you with a voice message.

---

## PART 7 — How to Talk to FRIDAY

Once FRIDAY is running:

1. Press `Ctrl+Alt+Space` from **anywhere** on your laptop — any app, any window
2. Speak your command or question clearly after the terminal shows "Listening..."
3. Stop talking — FRIDAY will automatically detect when you're done
4. FRIDAY will respond with voice and also perform the action if it's a command

**Commands you can say:**

| What you say | What happens |
|---|---|
| "Open VS Code" | VS Code launches |
| "Open Notepad" | Notepad launches |
| "Open Calculator" | Calculator launches |
| "Open Chrome" | Chrome browser opens |
| "Open Google" | Google.com opens in browser |
| "Search python tutorials on Google" | Searches Google for that query |
| "Initialize my setup" | Opens VS Code + all your profile tabs |
| Anything else | FRIDAY has a conversation with you |

**To stop FRIDAY:** Go back to the terminal and press `Ctrl+C`.

---

## 🛠️ Troubleshooting

**FRIDAY doesn't hear me / starts recording immediately without me speaking**
- Your microphone sensitivity or background noise may be too high
- Try speaking louder and closer to the mic
- Make sure no other app is using the microphone at the same time

**LLM responses are very slow**
- Close background apps (especially Chrome tabs) to free up RAM
- Make sure nothing else heavy is running alongside FRIDAY
- Qwen2.5:3b needs about 3-4GB RAM — on 8GB machines, keep other apps minimal

**"ollama: command not found" or Qwen doesn't respond**
- Make sure Ollama is running — open a separate CMD and run `ollama serve`
- Verify the model is downloaded: `ollama list` — you should see `qwen2.5:3b`

**Hotkey doesn't work from other apps**
- Make sure you ran Command Prompt as Administrator
- The `keyboard` library requires admin rights to listen globally across all windows

**PyAudio installation fails**
- Use the alternative method:
  ```bash
  pip install pipwin
  pipwin install pyaudio
  ```

**Kokoro voice model not found error**
- Make sure both `.onnx` and `.bin` files are directly inside the `FRIDAY/` folder, not in a subfolder

---

## 📦 Full List of Things You Need to Download

Quick reference of everything covered in this guide:

| What | Link | Size |
|---|---|---|
| Python 3.10+ | [python.org/downloads](https://www.python.org/downloads/) | ~25MB |
| Ollama | [ollama.com/download](https://ollama.com/download) | ~50MB |
| Qwen2.5:3b model | via `ollama pull qwen2.5:3b` | ~2GB |
| Git | [git-scm.com/download/win](https://git-scm.com/download/win) | ~50MB |
| kokoro-v1.0.int8.onnx | [GitHub Releases](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0) | ~88MB |
| voices-v1.0.bin | [GitHub Releases](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0) | ~250MB |

Total download size: approximately **2.5GB**

---

*FRIDAY is an active project — more features and improvements are added regularly. Check the [README](README.md) for the latest status and roadmap.*
