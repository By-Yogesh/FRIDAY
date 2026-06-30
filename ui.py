import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext
import queue
import time

ctk.set_appearance_mode("dark")

BG       = "#0a0a0a"
CARD_BG  = "#0f1115"
BORDER   = "#1c1f26"
ACCENT   = "#00d4ff"
GREEN    = "#00ff88"
ORANGE   = "#ff8c00"
DIM      = "#2a2a2a"
TEXT     = "#e0e0e0"
SUBTEXT  = "#8a8f98"
MUTED    = "#444444"


class FridayUI:
    def __init__(self, root):
        self.root = root
        self.root.title("F.R.I.D.A.Y")
        self.root.configure(fg_color=BG)
        self.root.resizable(True, True)

        self.q             = queue.Queue()
        self.state         = "idle"
        self.pulse         = 0
        self.pulse_dir     = 1
        self.text_callback = None
        self.camera_toggle_callback = None
        self._photo_ref = None

        self._build()
        self._animate()
        self._tick_clock()
        self._poll()

        self.root.after(10, self._maximize)

    def _maximize(self):
        try:
            self.root.update_idletasks()
            self.root.state('zoomed')
        except Exception:
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            self.root.geometry(f"{sw}x{sh}+0+0")

    def set_text_callback(self, fn):
        self.text_callback = fn

    # ---------------------------------------------------------
    # LAYOUT
    # ---------------------------------------------------------
    def _build(self):
        self._build_topbar()

        body = ctk.CTkFrame(self.root, fg_color=BG)
        body.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self._build_left_sidebar(body)
        self._build_right_panel(body)
        self._build_center(body)

    def _build_topbar(self):
        bar = ctk.CTkFrame(self.root, fg_color=BG, height=54)
        bar.pack(fill="x", padx=18, pady=(16, 8))

        left = ctk.CTkFrame(bar, fg_color="transparent")
        left.pack(side="left")
        ctk.CTkLabel(left, text="F.R.I.D.A.Y", font=("Courier New", 22, "bold"),
                     text_color=ACCENT).pack(side="left")
        dot = ctk.CTkLabel(left, text="●", font=("Arial", 10), text_color=GREEN)
        dot.pack(side="left", padx=(12, 4))
        ctk.CTkLabel(left, text="Online", font=("Courier New", 13),
                     text_color=SUBTEXT).pack(side="left")

        self.lbl_clock = ctk.CTkLabel(bar, text="--:--:--  |  -- -- ----",
                                      font=("Courier New", 13, "bold"), text_color=TEXT)
        self.lbl_clock.pack(side="left", expand=True)

        right = ctk.CTkFrame(bar, fg_color="transparent")
        right.pack(side="right")
        self.lbl_weather = ctk.CTkLabel(right, text="--°C   --",
                                        font=("Courier New", 13, "bold"), text_color=TEXT)
        self.lbl_weather.pack(side="left", padx=(0, 16))
        ctk.CTkButton(right, text="⚙", width=32, height=32, fg_color=CARD_BG,
                      hover_color=BORDER, text_color=SUBTEXT,
                      command=lambda: None).pack(side="left")

    def _card(self, parent, title):
        card = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=10,
                            border_width=1, border_color=BORDER)
        card.pack(fill="x", pady=(0, 10))
        head = ctk.CTkFrame(card, fg_color="transparent")
        head.pack(fill="x", padx=12, pady=(10, 4))
        ctk.CTkLabel(head, text=title, font=("Courier New", 11, "bold"),
                     text_color=TEXT).pack(side="left")
        return card

    def _build_left_sidebar(self, parent):
        side = ctk.CTkFrame(parent, fg_color=BG, width=300)
        side.pack(side="left", fill="y", padx=(0, 15))
        side.pack_propagate(False)

        c1 = self._card(side, "SYSTEM STATS")

        self.lbl_cpu = ctk.CTkLabel(c1, text="CPU Usage", font=("Courier New", 10, "bold"),
                                    text_color=SUBTEXT) 
        self.lbl_cpu.pack(anchor="w", padx=15, pady=(0, 12))
        self.bar_cpu = ctk.CTkProgressBar(c1, height=6, fg_color="#1a1d24",
                                          progress_color=ACCENT)
        self.bar_cpu.set(0)
        self.bar_cpu.pack(fill="x", padx=15, pady=(0, 12))

        self.lbl_ram = ctk.CTkLabel(c1, text="RAM Usage", font=("Courier New", 10, "bold"),
                                    text_color=SUBTEXT)
        self.lbl_ram.pack(anchor="w", padx=15, pady=(0, 12))
        self.bar_ram = ctk.CTkProgressBar(c1, height=6, fg_color="#1a1d24",
                                          progress_color=GREEN)
        self.bar_ram.set(0)
        self.bar_ram.pack(fill="x", padx=15, pady=(0, 12))

        stat_row = ctk.CTkFrame(c1, fg_color="transparent")
        stat_row.pack(fill="x", padx=15, pady=(5, 15))
        self.lbl_cpu_val = ctk.CTkLabel(stat_row, text="CPU\n--%", font=("Courier New", 13, "bold"),
                                        text_color=TEXT, justify="left")
        self.lbl_cpu_val.pack(side="left", expand=True)
        self.lbl_ram_val = ctk.CTkLabel(stat_row, text="Memory\n--%", font=("Courier New", 13, "bold"),
                                        text_color=TEXT, justify="left")
        self.lbl_ram_val.pack(side="left", expand=True)
        self.lbl_disk_val = ctk.CTkLabel(stat_row, text="Disk\n--/-- GB", font=("Courier New", 13, "bold"),
                                         text_color=TEXT, justify="left")
        self.lbl_disk_val.pack(side="left", expand=True)

        c2 = self._card(side, "WEATHER")

        top_row = ctk.CTkFrame(c2, fg_color="transparent")
        top_row.pack(fill="x", padx=12, pady=(2, 10))

        left_w = ctk.CTkFrame(top_row, fg_color="transparent")
        left_w.pack(side="left")
        self.lbl_w_temp = ctk.CTkLabel(left_w, text="--°C", font=("Courier New", 22, "bold"),
                                       text_color=TEXT)
        self.lbl_w_temp.pack(anchor="w")
        self.lbl_w_city = ctk.CTkLabel(left_w, text="--", font=("Courier New", 11, "bold"),
                                       text_color=SUBTEXT)
        self.lbl_w_city.pack(anchor="w")
        self.lbl_w_cond = ctk.CTkLabel(left_w, text="--", font=("Courier New", 11, "bold"),
                                       text_color=MUTED)
        self.lbl_w_cond.pack(anchor="w")

        stat_row3 = ctk.CTkFrame(c2, fg_color="transparent")
        stat_row3.pack(fill="x", padx=12, pady=(5, 15))
        self.lbl_humidity = ctk.CTkLabel(stat_row3, text="Humidity\n--%", font=("Courier New", 12, "bold"),
                                         text_color=TEXT, justify="left")
        self.lbl_humidity.pack(side="left", expand=True)
        self.lbl_wind = ctk.CTkLabel(stat_row3, text="Wind\n-- m/s", font=("Courier New", 12, "bold"),
                                     text_color=TEXT, justify="left")
        self.lbl_wind.pack(side="left", expand=True)
        self.lbl_feels = ctk.CTkLabel(stat_row3, text="Feels Like\n--°C", font=("Courier New", 12, "bold"),
                                      text_color=TEXT, justify="left")
        self.lbl_feels.pack(side="left", expand=True)

        c3 = ctk.CTkFrame(side, fg_color=CARD_BG, corner_radius=10,
                          border_width=1, border_color=BORDER)
        c3.pack(fill="x", pady=(2, 12))

        head3 = ctk.CTkFrame(c3, fg_color="transparent")
        head3.pack(fill="x", padx=12, pady=(10, 4))
        ctk.CTkLabel(head3, text="CAMERA", font=("Courier New", 12, "bold"),
                     text_color=TEXT).pack(side="left")
        self.btn_camera_toggle = ctk.CTkButton(head3, text="⏻", width=26, height=26,
                                               fg_color=CARD_BG, hover_color=BORDER,
                                               text_color=SUBTEXT,
                                               command=self._on_camera_btn)
        self.btn_camera_toggle.pack(side="right")

        cam_box = ctk.CTkFrame(c3, fg_color="#0a0c0f", corner_radius=8, height=140)
        cam_box.pack(fill="x", padx=12, pady=(2, 10))
        cam_box.pack_propagate(False)

        self.lbl_camera_feed = tk.Label(cam_box, bg="#0a0c0f", bd=0)
        self.lbl_camera_feed.pack(expand=True, fill="both")

        self.lbl_camera_placeholder = ctk.CTkLabel(cam_box, text="Camera Off",
                                                    font=("Courier New", 10),
                                                    text_color=MUTED)
        self.lbl_camera_placeholder.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_camera_status = ctk.CTkLabel(
            c3, text="Camera is inactive. Click the power button to start.",
            font=("Courier New", 12), text_color=MUTED,
            wraplength=220, justify="left"
        )
        self.lbl_camera_status.pack(anchor="w", padx=12, pady=(5, 15))

        c4 = self._card(side, "SYSTEM UPTIME")

        self.lbl_uptime = ctk.CTkLabel(c4, text="00:00:00", font=("Courier New", 18, "bold"),
                                       text_color=ACCENT)
        self.lbl_uptime.pack(anchor="w", padx=12, pady=(0, 8))
        ctk.CTkLabel(c4, text="System running for", font=("Courier New", 12),
                     text_color=MUTED).pack(anchor="w", padx=12, pady=(0, 8))

        stat_row2 = ctk.CTkFrame(c4, fg_color="transparent")
        stat_row2.pack(fill="x", padx=12, pady=(0, 7))
        self.lbl_session_val = ctk.CTkLabel(stat_row2, text="Session\n1", font=("Courier New", 12, "bold"),
                                            text_color=TEXT, justify="left")
        self.lbl_session_val.pack(side="left", expand=True)
        self.lbl_cmds_val = ctk.CTkLabel(stat_row2, text="Commands\n0", font=("Courier New", 12, "bold"),
                                         text_color=TEXT, justify="left")
        self.lbl_cmds_val.pack(side="left", expand=True)

        self.lbl_load = ctk.CTkLabel(c4, text="System Load", font=("Courier New", 12, "bold"),
                                     text_color=SUBTEXT)
        self.lbl_load.pack(anchor="w", padx=12, pady=(1, 7))
        self.bar_load = ctk.CTkProgressBar(c4, height=6, fg_color="#1a1d24",
                                           progress_color=ORANGE)
        self.bar_load.set(0)
        self.bar_load.pack(fill="x", padx=12, pady=(0, 4))
        self.lbl_load_val = ctk.CTkLabel(c4, text="Idle  0%", font=("Courier New", 12, "bold"),
                                         text_color=MUTED)
        self.lbl_load_val.pack(anchor="w", padx=12, pady=(0, 12))

    def _build_right_panel(self, parent):
        side = ctk.CTkFrame(parent, fg_color=CARD_BG, width=400,
                            corner_radius=10, border_width=1, border_color=BORDER)
        side.pack(side="right", fill="y")
        side.pack_propagate(False)

        head = ctk.CTkFrame(side, fg_color="transparent")
        head.pack(fill="x", padx=14, pady=(14, 8))
        ctk.CTkLabel(head, text="Conversation", font=("Courier New", 18),
                     text_color=TEXT).pack(side="left")
        ctk.CTkButton(head, text="Clear", width=54, height=24, fg_color="#1a1d24",
                      hover_color=BORDER, font=("Courier New", 12, "bold"),
                      command=self._clear_chat).pack(side="right", padx=(4, 0))
        ctk.CTkButton(head, text="Extract", width=60, height=24, fg_color="#1a1d24",
                      hover_color=BORDER, font=("Courier New", 12),
                      command=lambda: None).pack(side="right")

        self.chat = scrolledtext.ScrolledText(
            side, font=("Courier New", 10), bg=CARD_BG, fg=TEXT,
            insertbackground=ACCENT, selectbackground="#1e3a5f",
            relief="flat", wrap=tk.WORD, padx=12, pady=10,
            state="disabled", cursor="arrow", borderwidth=0, highlightthickness=0
        )
        self.chat.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        self.chat.tag_config("you_n", foreground=ACCENT, font=("Courier New", 10, "bold"))
        self.chat.tag_config("you_t", foreground=TEXT,    font=("Courier New", 12))
        self.chat.tag_config("fri_n", foreground=GREEN,   font=("Courier New", 10, "bold"))
        self.chat.tag_config("fri_t", foreground=SUBTEXT, font=("Courier New", 12))
        self.chat.tag_config("sys",   foreground=MUTED,   font=("Courier New", 10, "italic"))

        bottom = ctk.CTkFrame(side, fg_color="transparent")
        bottom.pack(fill="x", padx=10, pady=(0, 12))
        self.entry = ctk.CTkEntry(bottom, fg_color="#0a0c0f", border_color=BORDER,
                                  text_color=TEXT, placeholder_text="Type a message...",
                                  height=40, font=("Courier New", 10))
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self._on_send)
        ctk.CTkButton(bottom, text="➤", width=40, height=40, fg_color=ACCENT,
                      hover_color="#00a8cc", text_color="#001018",
                      command=self._on_send).pack(side="left", padx=(6, 0))

    def _build_center(self, parent):
        center = ctk.CTkFrame(parent, fg_color=BG)
        center.pack(side="left", fill="both", expand=True)

        ctk.CTkFrame(center, fg_color="transparent").pack(expand=True)

        self.canvas = tk.Canvas(center, width=170, height=170, bg=BG,
                                highlightthickness=0)
        self.canvas.pack()
        self.ring = self.canvas.create_oval(5, 5, 165, 165, outline=BORDER, width=1, fill="")
        self.orb  = self.canvas.create_oval(32, 32, 138, 138, fill=DIM, outline="", width=0)

        ctk.CTkLabel(center, text="F.R.I.D.A.Y", font=("Courier New", 22, "bold"),
                     text_color=ACCENT).pack(pady=(18, 8))

        self.lbl_state = ctk.CTkLabel(center, text="● Listening for hotkey...",
                                      font=("Courier New", 12), text_color=MUTED)
        self.lbl_state.pack()

        ctk.CTkFrame(center, fg_color="transparent").pack(expand=True)

        btn_row = ctk.CTkFrame(center, fg_color="transparent")
        btn_row.pack(pady=(0, 10))
        for label in ("📷", "🎙", "⌨"):
            b = ctk.CTkButton(btn_row, text=label, width=50, height=50,
                              corner_radius=24, fg_color=CARD_BG,
                              hover_color=BORDER, border_width=1, border_color=BORDER,
                              command=lambda l=label: self._on_bottom_btn(l))
            b.pack(side="left", padx=8)

    # ---------------------------------------------------------
    # BEHAVIOR
    # ---------------------------------------------------------
    def _on_bottom_btn(self, label):
        if label == "⌨":
            self.entry.focus()
        elif label == "📷":
            if self.camera_toggle_callback:
                self.camera_toggle_callback()
        elif label == "🎙":
            self.add_message("sys", "Use Ctrl+Alt+Space to talk to Friday.")

    def _clear_chat(self):
        self.chat.config(state="normal")
        self.chat.delete("1.0", "end")
        self.chat.config(state="disabled")

    def _on_send(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        if self.text_callback:
            self.text_callback(text)

    def _tick_clock(self):
        now = time.strftime("%I:%M:%S %p  |  %B %d, %Y")
        self.lbl_clock.configure(text=now)
        self.root.after(1000, self._tick_clock)

    def _animate(self):
        colors = {
            "idle":      (DIM,    BORDER),
            "listening": (ACCENT, ACCENT),
            "thinking":  (ORANGE, ORANGE),
            "speaking":  (GREEN,  GREEN),
        }
        orb_c, ring_c = colors.get(self.state, (DIM, BORDER))

        if self.state != "idle":
            self.pulse += self.pulse_dir * 1.8
            if self.pulse >= 18: self.pulse_dir = -1
            if self.pulse <= 0:  self.pulse_dir = 1
            p = self.pulse
            self.canvas.coords(self.ring, 5 - p, 5 - p, 165 + p, 165 + p)
            self.canvas.itemconfig(self.ring, outline=ring_c,
                                   width=max(1, int(1.5 * (1 - p / 18))))
        else:
            self.pulse, self.pulse_dir = 0, 1
            self.canvas.coords(self.ring, 5, 5, 165, 165)
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
                elif item[0] == "start":
                    self._do_start(item[1])
                elif item[0] == "append":
                    self._do_append(item[1])
                elif item[0] == "end":
                    self._do_end()
        except queue.Empty:
            pass
        self.root.after(50, self._poll)

    def _do_state(self, s):
        self.state = s
        cfg = {
            "idle":      ("● Listening for hotkey...", MUTED),
            "listening": ("● Listening...",            ACCENT),
            "thinking":  ("● Thinking...",              ORANGE),
            "speaking":  ("● Speaking...",               GREEN),
        }
        txt, col = cfg.get(s, ("● Idle", MUTED))
        self.lbl_state.configure(text=txt, text_color=col)

    def _do_msg(self, who, text):
        self.chat.config(state="normal")
        if who == "you":
            self.chat.insert("end", "\nYOU\n", "you_n")
            self.chat.insert("end", f"{text}\n", "you_t")
        elif who == "friday":
            self.chat.insert("end", "\nFRIDAY\n", "fri_n")
            self.chat.insert("end", f"{text}\n", "fri_t")
        else:
            self.chat.insert("end", f"\n{text}\n", "sys")
        self.chat.config(state="disabled")
        self.chat.see("end")

    def _do_start(self, who):
        self.chat.config(state="normal")
        if who == "friday":
            self.chat.insert("end", "\nFRIDAY\n", "fri_n")
        else:
            self.chat.insert("end", "\nYOU\n", "you_n")
        self.chat.config(state="disabled")
        self.chat.see("end")

    def _do_append(self, text):
        self.chat.config(state="normal")
        self.chat.insert("end", text, "fri_t")
        self.chat.config(state="disabled")
        self.chat.see("end")

    def _do_end(self):
        self.chat.config(state="normal")
        self.chat.insert("end", "\n")
        self.chat.config(state="disabled")

    def set_state(self, s):       self.q.put(("state", s))
    def add_message(self, w, t):  self.q.put(("msg", w, t))
    def update_stats(self, cpu_pct, ram_pct, ram_used_gb, ram_total_gb,
                      disk_used_gb, disk_total_gb):
        self.bar_cpu.set(cpu_pct / 100)
        self.bar_ram.set(ram_pct / 100)
        self.lbl_cpu_val.configure(text=f"CPU\n{cpu_pct:.0f}%")
        self.lbl_ram_val.configure(text=f"Memory\n{ram_pct:.0f}%")
        self.lbl_disk_val.configure(text=f"Disk\n{disk_used_gb:.0f}/{disk_total_gb:.0f} GB")

    def update_uptime(self, uptime_str, commands_count, load_pct):
        self.lbl_uptime.configure(text=uptime_str)
        self.lbl_cmds_val.configure(text=f"Commands\n{commands_count}")
        self.bar_load.set(load_pct / 100)

        label = "Idle"
        if load_pct > 70:
            label = "High"
        elif load_pct > 30:
            label = "Moderate"
        self.lbl_load_val.configure(text=f"{label}  {load_pct:.0f}%")

    def set_camera_toggle_callback(self, fn):
        self.camera_toggle_callback = fn

    def _on_camera_btn(self):
        if self.camera_toggle_callback:
            self.camera_toggle_callback()

    def update_camera_frame(self, photo_image):
        self._photo_ref = photo_image
        self.lbl_camera_feed.configure(image=photo_image)
        self.lbl_camera_placeholder.place_forget()

    def set_camera_state(self, active):
        if active:
            self.lbl_camera_status.configure(text="Camera is active.")
            self.btn_camera_toggle.configure(text_color=GREEN)
        else:
            self.lbl_camera_feed.configure(image="")
            self.lbl_camera_placeholder.place(relx=0.5, rely=0.5, anchor="center")
            self.lbl_camera_status.configure(
                text="Camera is inactive. Click the power button to start.")
            self.btn_camera_toggle.configure(text_color=SUBTEXT)

    def update_weather(self, temp, feels_like, humidity, wind, condition, city):
        self.lbl_w_temp.configure(text=f"{temp:.1f}°C")
        self.lbl_w_city.configure(text=city)
        self.lbl_w_cond.configure(text=condition)
        self.lbl_humidity.configure(text=f"Humidity\n{humidity}%")
        self.lbl_wind.configure(text=f"Wind\n{wind} m/s")
        self.lbl_feels.configure(text=f"Feels Like\n{feels_like:.1f}°C")

        # Also update the top bar weather display
        self.lbl_weather.configure(text=f"{temp:.1f}°C   {city}")
    def start_message(self, who): self.q.put(("start", who))
    def append_text(self, text):  self.q.put(("append", text))
    def end_message(self):        self.q.put(("end",))