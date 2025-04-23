import os
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox

# Playback backend: try pygame first, fall back to winsound on Windows
try:
    import pygame
    pygame.mixer.init()
    def play_sound(path):
        pygame.mixer.Sound(path).play()
except ImportError:
    import winsound
    def play_sound(path):
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)

class Soundboard(tk.Tk):
    SHORTCUT_KEYS = ["1","2","3","4","5","6","7","8","9","0"]

    def __init__(self):
        super().__init__()
        self.title("Soundboard")
        self.geometry("650x800")

        self.sounds = []    # list of {"name":…, "path":…}
        self.shortcuts = {} # map "1".."0" → index in self.sounds

        self._build_shortcut_frame()
        self._build_control_frame()
        self._build_list_frame()

        # Catch every keypress globally
        self.bind_all("<KeyPress>", self._on_keypress)
        self.focus_set()

    def _build_shortcut_frame(self):
        frm = ttk.LabelFrame(self, text="Quick-Access Shortcuts (Shift+1…0)")
        frm.pack(fill="x", padx=10, pady=10)

        self.shortcut_buttons = {}
        for i, key in enumerate(self.SHORTCUT_KEYS):
            btn = ttk.Button(frm, text=f"{key}: ---",
                             command=lambda k=key: self._play_shortcut(k))
            btn.grid(row=0, column=i, padx=3, pady=5, sticky="ew")
            frm.columnconfigure(i, weight=1)
            self.shortcut_buttons[key] = btn

    def _build_control_frame(self):
        frm = ttk.Frame(self)
        frm.pack(fill="x", padx=10, pady=(0,10))
        load_btn = ttk.Button(frm, text="➕ Load Sound", command=self.load_sound)
        load_btn.pack(side="left")

    def _build_list_frame(self):
        lf = ttk.LabelFrame(self, text="All Loaded Sounds")
        lf.pack(fill="both", expand=True, padx=10, pady=(0,10))

        canvas = tk.Canvas(lf)
        scrollbar = ttk.Scrollbar(lf, orient="vertical", command=canvas.yview)
        self.inner = ttk.Frame(canvas)

        self.inner.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0,0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.update_list()

    def load_sound(self):
        if len(self.sounds) >= 100:
            messagebox.showwarning("Limit reached", "You can only load up to 100 sounds.")
            return

        path = filedialog.askopenfilename(
            filetypes=[("Audio files", "*.wav *.mp3 *.ogg *.flac")]
        )
        if not path:
            return

        name = simpledialog.askstring("Name this sound", "Enter a display name:")
        if not name:
            name = os.path.basename(path)

        self.sounds.append({"name": name, "path": path})
        self.update_list()

    def update_list(self):
        for w in self.inner.winfo_children():
            w.destroy()

        for idx, snd in enumerate(self.sounds):
            lbl = ttk.Label(self.inner, text=snd["name"], width=30)
            lbl.grid(row=idx, column=0, padx=5, pady=2, sticky="w")

            play_btn = ttk.Button(self.inner, text="▶ Play",
                                  command=lambda i=idx: self.play(i))
            play_btn.grid(row=idx, column=1, padx=5, pady=2)

            assign_btn = ttk.Button(self.inner, text="🔑 Assign",
                                    command=lambda i=idx: self.assign_shortcut(i))
            assign_btn.grid(row=idx, column=2, padx=5, pady=2)

    def play(self, idx):
        play_sound(self.sounds[idx]["path"])

    def _on_keypress(self, event):
        # Check Shift bit (0x0001 on Windows) and digit keycodes
        if not (event.state & 0x0001):
            return

        code = event.keycode
        # keycodes 49–57 = '1'–'9', 48 = '0'
        if 49 <= code <= 57:
            key = str(code - 48)
        elif code == 48:
            key = "0"
        else:
            return

        self._play_shortcut(key)

    def _play_shortcut(self, key):
        if key in self.shortcuts:
            self.play(self.shortcuts[key])
        else:
            messagebox.showinfo("No shortcut", f"No sound assigned to Shift+{key}")

    def assign_shortcut(self, idx):
        key = simpledialog.askstring(
            "Assign Shortcut",
            "Choose a slot (1–9 or 0) for this sound:"
        )
        if key not in self.SHORTCUT_KEYS:
            messagebox.showerror("Invalid key", "Must be one of 1–9 or 0.")
            return

        self.shortcuts[key] = idx
        self._refresh_shortcut_buttons()

    def _refresh_shortcut_buttons(self):
        for key, btn in self.shortcut_buttons.items():
            if key in self.shortcuts:
                name = self.sounds[self.shortcuts[key]]["name"]
            else:
                name = "---"
            btn.config(text=f"{key}: {name}")

if __name__ == "__main__":
    app = Soundboard()
    app.mainloop()
