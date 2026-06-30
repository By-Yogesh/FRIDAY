import tkinter as tk
from tkinter import scrolledtext
import queue

BG      = "#0a0a0a"
PANEL   = "#0d0d0d"
BORDER  = "#1a1a1a"
ACCENT  = "#00d4ff"
GREEN   = "#00ff88"
ORANGE  = "#ff8c00"
DIM     = "#2a2a2a"
TEXT    = "#e0e0e0"
SUBTEXT = "#999999"
MUTED   = "#444444"

class FridayUI:
    def __init__(self, root):
        self.root = root
        self.root.title("F.R.I.D.A.Y")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self._center(700, 700)

        self.q             = queue.Queue()
        self.state         = "idle"
        self.pulse         = 0
        self.pulse_dir     = 1
        self.text_callback = None

        self._build()
        self._animate()
        self._poll()

    def _center(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def set_text_callback(self, fn):
        self.text_callback = fn

    def _on_send(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        if self.text_callback:
            self.text_callback(text)

    def _build(self):
        # Header
        tk.Frame(self.root, bg=BG, height=22).pack()
        tk.Label(self.root, text="F.R.I.D.A.Y",
                 font=("Courier New", 24, "bold"),
                 fg=ACCENT, bg=BG).pack()
        tk.Label(self.root, text="Personal AI Assistant",
                 font=("Courier New", 9),
                 fg="#2a2a2a", bg=BG).pack(pady=(3, 0))

        # Divider
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=30, pady=18)

        # Orb
        self.canvas = tk.Canvas(self.root, width=110, height=110,
                                bg=BG, highlightthickness=0)
        self.canvas.pack()
        self.ring = self.canvas.create_oval(5, 5, 105, 105,
                                            outline=BORDER, width=1, fill="")
        self.orb  = self.canvas.create_oval(20, 20, 90, 90,
                                            fill=DIM, outline="", width=0)

        # State + hint labels
        self.lbl_state = tk.Label(self.root, text="IDLE",
                                  font=("Courier New", 11, "bold"),
                                  fg=MUTED, bg=BG)
        self.lbl_state.pack(pady=(12, 2))

        self.lbl_hint = tk.Label(self.root,
                                 text="Press Ctrl+Alt+Space to talk",
                                 font=("Courier New", 8),
                                 fg="#2a2a2a", bg=BG)
        self.lbl_hint.pack()

        # Divider
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=30, pady=14)

        # Conversation label
        tk.Label(self.root, text="CONVERSATION",
                 font=("Courier New", 8),
                 fg="#2a2a2a", bg=BG).pack(anchor="w", padx=34, pady=(0, 6))

        # Chat box
        outer = tk.Frame(self.root, bg=BORDER)
        outer.pack(fill="both", expand=True, padx=28)
        inner = tk.Frame(outer, bg=PANEL)
        inner.pack(fill="both", expand=True, padx=1, pady=1)

        self.chat = scrolledtext.ScrolledText(
            inner,
            font=("Courier New", 9),
            bg=PANEL, fg=TEXT,
            insertbackground=ACCENT,
            selectbackground="#1e3a5f",
            relief="flat", wrap=tk.WORD,
            padx=14, pady=14,
            state="disabled",
            cursor="arrow",
            borderwidth=0
        )
        self.chat.pack(fill="both", expand=True)

        self.chat.tag_config("you_n", foreground=ACCENT,   font=("Courier New", 8, "bold"))
        self.chat.tag_config("you_t", foreground=TEXT,      font=("Courier New", 9))
        self.chat.tag_config("fri_n", foreground=GREEN,     font=("Courier New", 8, "bold"))
        self.chat.tag_config("fri_t", foreground=SUBTEXT,   font=("Courier New", 9))
        self.chat.tag_config("sys",   foreground="#2a2a2a", font=("Courier New", 8, "italic"))

        # ── Text input bar ──────────────────────────────────────
        input_wrap = tk.Frame(self.root, bg=BG)
        input_wrap.pack(fill="x", padx=28, pady=(10, 0))

        border_frame = tk.Frame(input_wrap, bg=BORDER)
        border_frame.pack(fill="x")

        inner_frame = tk.Frame(border_frame, bg="#111111")
        inner_frame.pack(fill="x", padx=1, pady=1)

        self.entry = tk.Entry(
            inner_frame,
            font=("Courier New", 10),
            bg="#111111", fg=TEXT,
            insertbackground=ACCENT,
            relief="flat", borderwidth=0
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=14, pady=11)
        self.entry.bind("<Return>", self._on_send)

        tk.Button(
            inner_frame,
            text="SEND",
            font=("Courier New", 8, "bold"),
            fg=ACCENT, bg="#111111",
            activebackground="#1a1a1a",
            activeforeground=ACCENT,
            relief="flat", borderwidth=0,
            cursor="hand2",
            padx=16, pady=11,
            command=self._on_send
        ).pack(side="right")
        # ────────────────────────────────────────────────────────

        # Footer
        tk.Label(self.root,
                 text="FRIDAY v1.0  •  Local AI  •  Fully Offline",
                 font=("Courier New", 7),
                 fg="#1a1a1a", bg=BG).pack(pady=(8, 12))

    def _animate(self):
        colors = {
            "idle":      (DIM,    BORDER),
            "listening": (ACCENT, ACCENT),
            "thinking":  (ORANGE, ORANGE),
            "speaking":  (GREEN,  GREEN),
        }
        orb_c, ring_c = colors.get(self.state, (DIM, BORDER))

        if self.state != "idle":
            self.pulse += self.pulse_dir * 1.5
            if self.pulse >= 16: self.pulse_dir = -1
            if self.pulse <= 0:  self.pulse_dir =  1
            p = self.pulse
            self.canvas.coords(self.ring, 5-p, 5-p, 105+p, 105+p)
            self.canvas.itemconfig(self.ring, outline=ring_c,
                                   width=max(1, int(1.5*(1-p/16))))
        else:
            self.pulse     = 0
            self.pulse_dir = 1
            self.canvas.coords(self.ring, 5, 5, 105, 105)
            self.canvas.itemconfig(self.ring, outline=BORDER, width=1)

        self.canvas.itemconfig(self.orb, fill=orb_c)
        self.root.after(30, self._animate)

    def _poll(self):
        try:
            while True:
                item = self.q.get_nowait()
                if item[0] == "state":
                    self._do_state(item[1])
                elif item[0] == "msg":
                    self._do_msg(item[1], item[2])
        except queue.Empty:
            pass
        self.root.after(80, self._poll)

    def _do_state(self, s):
        self.state = s
        cfg = {
            "idle":      ("IDLE",      MUTED,  "Press Ctrl+Alt+Space to talk  |  or type below"),
            "listening": ("LISTENING", ACCENT, "Speak now..."),
            "thinking":  ("THINKING",  ORANGE, "Processing..."),
            "speaking":  ("SPEAKING",  GREEN,  "Friday is responding..."),
        }
        txt, col, hint = cfg.get(s, ("IDLE", MUTED, ""))
        self.lbl_state.config(text=txt, fg=col)
        self.lbl_hint.config(text=hint)

    def _do_msg(self, who, text):
        self.chat.config(state="normal")
        if who == "you":
            self.chat.insert("end", "\nYOU\n",     "you_n")
            self.chat.insert("end", f"{text}\n",   "you_t")
        elif who == "friday":
            self.chat.insert("end", "\nFRIDAY\n",  "fri_n")
            self.chat.insert("end", f"{text}\n",   "fri_t")
        else:
            self.chat.insert("end", f"\n{text}\n", "sys")
        self.chat.config(state="disabled")
        self.chat.see("end")

    def set_state(self, s):       self.q.put(("state", s))
    def add_message(self, w, t):  self.q.put(("msg",   w, t))