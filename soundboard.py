import os
import json
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox

# Playback backend: try pygame, else winsound on Windows
try:
    import pygame
    pygame.mixer.init()
    def play_sound(path):
        pygame.mixer.Sound(path).play()
except ImportError:
    import winsound
    def play_sound(path):
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)

# Global hotkey support
try:
    import keyboard
    GLOBAL_HOTKEYS = True
except ImportError:
    GLOBAL_HOTKEYS = False
    print("⚠️  Install 'keyboard' if you want Ctrl+number to work globally.")

# Constants
SAVEDIR = os.path.join(os.getcwd(), "SavedSounds")
CONFIG_PATH = os.path.join(SAVEDIR, "config.json")
AUDIO_EXTS = {".wav", ".mp3", ".ogg", ".flac"}

class Soundboard(tk.Tk):
    SHORTCUT_KEYS = ["1","2","3","4","5","6","7","8","9","0"]

    def __init__(self):
        super().__init__()
        self.title("Soundboard")
        self.geometry("650x800")

        # In-memory state
        self.sounds = []      # list of dicts: {"filename","name","path"}
        self.shortcuts = {}   # map "1".."0" → filename

        # Load previous state (creates folder+config if needed)
        self._load_config()

        # Build UI
        self._build_shortcut_frame()
        self._build_control_frame()
        self._build_list_frame()

        # Register global Ctrl+number if possible
        if GLOBAL_HOTKEYS:
            self._register_global_hotkeys()

        # Ensure Tk window has focus for fallback
        self.focus_set()

    def _load_config(self):
        os.makedirs(SAVEDIR, exist_ok=True)

        # read config.json if exists
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"sounds": [], "shortcuts": {}}

        # build a map filename→custom name
        name_map = {s["filename"]: s["name"] for s in data.get("sounds", [])}

        # scan folder for audio files
        files = sorted(f for f in os.listdir(SAVEDIR)
                       if os.path.splitext(f)[1].lower() in AUDIO_EXTS)
        for fn in files:
            path = os.path.join(SAVEDIR, fn)
            display_name = name_map.get(fn, os.path.splitext(fn)[0])
            self.sounds.append({
                "filename": fn,
                "name": display_name,
                "path": path
            })

        # load shortcuts (only keep ones whose file still exists)
        for key, fn in data.get("shortcuts", {}).items():
            if fn in files and key in self.SHORTCUT_KEYS:
                self.shortcuts[key] = fn

        # rewrite config (in case new files were added manually)
        self._save_config()

    def _save_config(self):
        data = {
            "sounds": [
                {"filename": s["filename"], "name": s["name"]}
                for s in self.sounds
            ],
            "shortcuts": self.shortcuts
        }
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _build_shortcut_frame(self):
        frm = ttk.LabelFrame(self, text="Quick-Access (Ctrl+1…0)")
        frm.pack(fill="x", padx=10, pady=10)

        self.shortcut_buttons = {}
        for i, key in enumerate(self.SHORTCUT_KEYS):
            btn = ttk.Button(frm, text=f"{key}: ---",
                             command=lambda k=key: self._play_shortcut(k))
            btn.grid(row=0, column=i, padx=3, pady=5, sticky="ew")
            frm.columnconfigure(i, weight=1)
            self.shortcut_buttons[key] = btn
        self._refresh_shortcut_buttons()

    def _build_control_frame(self):
        frm = ttk.Frame(self)
        frm.pack(fill="x", padx=10, pady=(0,10))
        ttk.Button(frm, text="➕ Load Sound", command=self.load_sound)\
            .pack(side="left")

    def _build_list_frame(self):
        lf = ttk.LabelFrame(self, text="All Loaded Sounds")
        lf.pack(fill="both", expand=True, padx=10, pady=(0,10))

        canvas = tk.Canvas(lf)
        scrollbar = ttk.Scrollbar(lf, orient="vertical", command=canvas.yview)
        self.inner = ttk.Frame(canvas)

        self.inner.bind("<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.update_list()

    def _register_global_hotkeys(self):
        for key in self.SHORTCUT_KEYS:
            keyboard.add_hotkey(f"ctrl+{key}",
                                lambda k=key: self._play_shortcut(k))

    def load_sound(self):
        if len(self.sounds) >= 100:
            messagebox.showwarning("Limit reached",
                                   "You can only load up to 100 sounds.")
            return

        path = filedialog.askopenfilename(
            filetypes=[("Audio files","*.wav *.mp3 *.ogg *.flac")]
        )
        if not path:
            return

        # ask for display name
        name = simpledialog.askstring("Name this sound",
                                      "Enter a display name:")
        if not name:
            name = os.path.basename(path)

        # copy into SavedSounds
        fn = os.path.basename(path)
        dest = os.path.join(SAVEDIR, fn)
        base, ext = os.path.splitext(fn)
        counter = 1
        while os.path.exists(dest):
            fn = f"{base}({counter}){ext}"
            dest = os.path.join(SAVEDIR, fn)
            counter += 1
        shutil.copy2(path, dest)

        # add to list and save
        self.sounds.append({"filename": fn, "name": name, "path": dest})
        self._save_config()
        self.update_list()
        self._refresh_shortcut_buttons()

    def update_list(self):
        for w in self.inner.winfo_children():
            w.destroy()

        for idx, snd in enumerate(self.sounds):
            ttk.Label(self.inner, text=snd["name"], width=30)\
               .grid(row=idx, column=0, padx=5, pady=2, sticky="w")

            ttk.Button(self.inner, text="▶ Play",
                       command=lambda i=idx: self.play(i))\
               .grid(row=idx, column=1, padx=5, pady=2)

            ttk.Button(self.inner, text="🔑 Assign",
                       command=lambda i=idx: self.assign_shortcut(i))\
               .grid(row=idx, column=2, padx=5, pady=2)

            ttk.Button(self.inner, text="🗑 Delete",
                       command=lambda i=idx: self.delete_sound(i))\
               .grid(row=idx, column=3, padx=5, pady=2)

    def play(self, idx):
        play_sound(self.sounds[idx]["path"])

    def _play_shortcut(self, key):
        fn = self.shortcuts.get(key)
        if not fn:
            return  # unassigned slot
        for idx, snd in enumerate(self.sounds):
            if snd["filename"] == fn:
                self.play(idx)
                return

    def assign_shortcut(self, idx):
        key = simpledialog.askstring("Assign Shortcut",
                                     "Choose a slot (1–9 or 0):")
        if key not in self.SHORTCUT_KEYS:
            messagebox.showerror("Invalid key", "Must be 1–9 or 0.")
            return
        self.shortcuts[key] = self.sounds[idx]["filename"]
        self._save_config()
        self._refresh_shortcut_buttons()

    def delete_sound(self, idx):
        snd = self.sounds[idx]
        if not messagebox.askyesno("Delete",
                                   f"Remove '{snd['name']}' forever?"):
            return
        # remove file
        try:
            os.remove(snd["path"])
        except OSError as e:
            messagebox.showerror("Error", f"Could not delete file:\n{e}")
            return
        # clean up lists & shortcuts
        fn = snd["filename"]
        self.sounds.pop(idx)
        for k, v in list(self.shortcuts.items()):
            if v == fn:
                del self.shortcuts[k]
        self._save_config()
        self.update_list()
        self._refresh_shortcut_buttons()

    def _refresh_shortcut_buttons(self):
        for key, btn in self.shortcut_buttons.items():
            fn = self.shortcuts.get(key)
            name = next((s["name"] for s in self.sounds if s["filename"]==fn), "---")
            btn.config(text=f"{key}: {name}")

if __name__ == "__main__":
    app = Soundboard()
    app.mainloop()
