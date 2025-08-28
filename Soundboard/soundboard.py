import os, json, shutil, math
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox

try:
    import pygame
    pygame.mixer.init()
    def _default_play(path, vol=1.0):
        snd = pygame.mixer.Sound(path)
        snd.set_volume(vol)
        snd.play()
except ImportError:
    import winsound
    def _default_play(path, vol=1.0):
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)

try:
    import sounddevice as sd
    import soundfile as sf
    SD_AVAILABLE = True
except ImportError:
    SD_AVAILABLE = False

try:
    import keyboard
    GLOBAL_HOTKEYS = True
except ImportError:
    GLOBAL_HOTKEYS = False

SAVEDIR = os.path.join(os.getcwd(), "SavedSounds")
CONFIG_PATH = os.path.join(SAVEDIR, "config.json")
AUDIO_EXTS = {".wav", ".mp3", ".ogg", ".flac"}

class Soundboard(tk.Tk):
    SHORTCUT_KEYS = list("1234567890")

    def __init__(self):
        super().__init__()
        self.title("Soundboard")
        self.geometry("750x900")

        self._scan_devices()

        self.sounds = []
        self.shortcuts = {}
        self.use_mic_var = tk.BooleanVar()
        self.route_dev_var = tk.StringVar()
        self.play_vol_var = tk.DoubleVar()
        self.vm_mode_var = tk.BooleanVar()
        self.mic_level_var = tk.DoubleVar(value=0.0)

        os.makedirs(SAVEDIR, exist_ok=True)
        self._load_config()

        self._build_settings_frame()
        self._build_shortcut_frame()
        self._build_control_frame()
        self._build_list_frame()

        if GLOBAL_HOTKEYS:
            for k in self.SHORTCUT_KEYS:
                keyboard.add_hotkey(f"ctrl+{k}", lambda k=k: self._play_shortcut(k))

        if SD_AVAILABLE:
            try:
                self._mic_stream = sd.InputStream(device=None, channels=1, callback=self._mic_cb)
                self._mic_stream.start()
            except Exception as e:
                print("Mic stream error:", e)

        self.focus_set()

    def _scan_devices(self):
        if SD_AVAILABLE:
            all_devs = sd.query_devices()
            self.device_options_output = [d["name"] for d in all_devs if d["max_output_channels"] > 0]
            self.device_map_output = {d["name"]: i for i, d in enumerate(all_devs) if d["max_output_channels"] > 0}
        else:
            self.device_options_output = []
            self.device_map_output = {}

    def _load_config(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        else:
            cfg = {"sounds": [], "shortcuts": {}, "use_mic": False,
                   "route_device": None, "play_volume": 100.0, "vm_mode": False}

        name_map = {s["filename"]: s["name"] for s in cfg.get("sounds", [])}
        files = sorted(fn for fn in os.listdir(SAVEDIR) if os.path.splitext(fn)[1].lower() in AUDIO_EXTS)
        for fn in files:
            self.sounds.append({
                "filename": fn,
                "name": name_map.get(fn, os.path.splitext(fn)[0]),
                "path": os.path.join(SAVEDIR, fn)
            })

        self.shortcuts = {k: v for k, v in cfg.get("shortcuts", {}).items()
                          if k in self.SHORTCUT_KEYS and v in [s["filename"] for s in self.sounds]}

        self.use_mic_var.set(cfg.get("use_mic", False))
        self.route_dev_var.set(cfg.get("route_device") if cfg.get("route_device") in self.device_options_output
                               else (self.device_options_output[0] if self.device_options_output else ""))
        self.play_vol_var.set(cfg.get("play_volume", 100.0))
        self.vm_mode_var.set(cfg.get("vm_mode", False))

    def _save_config(self):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump({
                "sounds": [{"filename": s["filename"], "name": s["name"]} for s in self.sounds],
                "shortcuts": self.shortcuts,
                "use_mic": self.use_mic_var.get(),
                "route_device": self.route_dev_var.get(),
                "play_volume": self.play_vol_var.get(),
                "vm_mode": self.vm_mode_var.get()
            }, f, indent=2)

    def _build_settings_frame(self):
        frm = ttk.LabelFrame(self, text="Settings & Test Meters")
        frm.pack(fill="x", padx=10, pady=10)

        ttk.Label(frm, text="Route Output → Mic device:").grid(row=0, column=0, sticky="w")
        self.route_output_combo = ttk.Combobox(frm, values=self.device_options_output,
                                               textvariable=self.route_dev_var, state="readonly", width=30)
        self.route_output_combo.grid(row=0, column=1, padx=5, sticky="w")
        self.route_output_combo.bind("<<ComboboxSelected>>", lambda e: self._save_config())

        ttk.Button(frm, text="🔄 Refresh Devices", command=self._refresh_devices).grid(row=0, column=2, padx=5)

        ttk.Label(frm, text="Playback Volume:").grid(row=1, column=0, sticky="w")
        ttk.Scale(frm, from_=0, to=100, variable=self.play_vol_var,
                  orient="horizontal", command=lambda e: self._save_config()).grid(row=1, column=1, padx=5, sticky="ew")

        ttk.Label(frm, text="Mic Level:").grid(row=2, column=0, sticky="w")
        ttk.Progressbar(frm, orient="horizontal", maximum=100,
                        variable=self.mic_level_var).grid(row=2, column=1, padx=5, sticky="ew")

        def enable_vm_mode():
            if self.vm_mode_var.get():
                if not any("CABLE Input" in d for d in self.device_options_output):
                    messagebox.showwarning("VB-CABLE Not Found",
                                           "VB-Audio Cable not detected.\nInstall from https://vb-audio.com/Cable/")
                    self.vm_mode_var.set(False)
                    return
                for dev in self.device_options_output:
                    if "CABLE Input" in dev:
                        self.route_dev_var.set(dev)
                        break
                messagebox.showinfo("VoiceMeeter Setup",
                                    "✅ Output set to 'CABLE Input'.\n\n🎤 In VoiceMeeter:\n"
                                    "1. Set your real mic in Input 1\n"
                                    "2. Set 'VoiceMeeter Output' as your Discord mic\n"
                                    "Now both mic + sounds will be heard.")
                self._save_config()
        ttk.Checkbutton(frm, text="Use Mic + Soundboard (VoiceMeeter Mode)",
                        variable=self.vm_mode_var, command=enable_vm_mode).grid(row=3, column=0, columnspan=3, pady=5, sticky="w")
        frm.columnconfigure(1, weight=1)

    def _refresh_devices(self):
        self._scan_devices()
        self.route_output_combo.config(values=self.device_options_output)
        if self.route_dev_var.get() not in self.device_options_output:
            self.route_dev_var.set(self.device_options_output[0] if self.device_options_output else "")
        self._save_config()

    def _build_shortcut_frame(self):
        frm = ttk.LabelFrame(self, text="Quick-Access Shortcuts (Ctrl+1…0)")
        frm.pack(fill="x", padx=10, pady=10)
        self.shortcut_buttons = {}
        for i, k in enumerate(self.SHORTCUT_KEYS):
            btn = ttk.Button(frm, text=f"{k}: ---", command=lambda k=k: self._play_shortcut(k))
            btn.grid(row=0, column=i, padx=2, pady=5, sticky="ew")
            frm.columnconfigure(i, weight=1)
            self.shortcut_buttons[k] = btn
        self._refresh_shortcuts()

    def _build_control_frame(self):
        frm = ttk.Frame(self)
        frm.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(frm, text="➕ Load Sound", command=self.load_sound).pack(side="left", padx=5)

    def _build_list_frame(self):
        lf = ttk.LabelFrame(self, text="All Loaded Sounds")
        lf.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        canvas = tk.Canvas(lf)
        scroll = ttk.Scrollbar(lf, orient="vertical", command=canvas.yview)
        self.inner = ttk.Frame(canvas)
        self.inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.update_list()

    def _mic_cb(self, indata, frames, time, status):
        total = sum(sample[0] ** 2 for sample in indata)
        rms = math.sqrt(total / len(indata)) if len(indata) > 0 else 0
        self.mic_level_var.set(min(rms * 300, 100))

    def load_sound(self):
        if len(self.sounds) >= 100:
            return messagebox.showwarning("Limit reached", "Max 100 sounds.")
        path = filedialog.askopenfilename(filetypes=[("Audio", "*.wav *.mp3 *.ogg *.flac")])
        if not path:
            return
        name = simpledialog.askstring("Name", "Enter display name:") or os.path.basename(path)
        fn = os.path.basename(path)
        base, ext = os.path.splitext(fn)
        dest = os.path.join(SAVEDIR, fn)
        i = 1
        while os.path.exists(dest):
            fn = f"{base}({i}){ext}"
            dest = os.path.join(SAVEDIR, fn)
            i += 1
        shutil.copy2(path, dest)
        self.sounds.append({"filename": fn, "name": name, "path": dest})
        self._save_config()
        self.update_list()
        self._refresh_shortcuts()

    def update_list(self):
        for w in self.inner.winfo_children():
            w.destroy()
        for i, s in enumerate(self.sounds):
            ttk.Label(self.inner, text=s["name"], width=30).grid(row=i, column=0, padx=5, pady=2, sticky="w")
            ttk.Button(self.inner, text="Play", command=lambda i=i: self.play(i)).grid(row=i, column=1, padx=5, pady=2)
            ttk.Button(self.inner, text="Assign", command=lambda i=i: self.assign(i)).grid(row=i, column=2, padx=5, pady=2)
            ttk.Button(self.inner, text="🗑 Delete", command=lambda i=i: self.delete(i)).grid(row=i, column=3, padx=5, pady=2)

    def delete(self, idx):
        s = self.sounds[idx]
        if not messagebox.askyesno("Delete", f"Remove '{s['name']}'?"):
            return
        try:
            os.remove(s["path"])
        except OSError as e:
            return messagebox.showerror("Err", e)
        fn = s["filename"]
        self.sounds.pop(idx)
        self.shortcuts = {k: v for k, v in self.shortcuts.items() if v != fn}
        self._save_config()
        self.update_list()
        self._refresh_shortcuts()

    def assign(self, idx):
        key = simpledialog.askstring("Assign", "Slot (1–9 or 0):")
        if key not in self.SHORTCUT_KEYS:
            return messagebox.showerror("Invalid", "Must be 1–9 or 0.")
        self.shortcuts[key] = self.sounds[idx]["filename"]
        self._save_config()
        self._refresh_shortcuts()

    def _refresh_shortcuts(self):
        for k, btn in self.shortcut_buttons.items():
            fn = self.shortcuts.get(k)
            nm = next((s["name"] for s in self.sounds if s["filename"] == fn), "---")
            btn.config(text=f"{k}: {nm}")

    def play(self, idx):
        s = self.sounds[idx]
        vol = float(self.play_vol_var.get()) / 100.0
        if self.use_mic_var.get() and SD_AVAILABLE and self.route_dev_var.get():
            try:
                data, fs = sf.read(s["path"], dtype="float32")
                data *= vol
                dev = self.device_map_output.get(self.route_dev_var.get())
                sd.check_output_settings(device=dev, samplerate=fs)
                sd.play(data, fs, device=dev)
            except Exception as e:
                messagebox.showerror("Playback Error", f"Could not play:\n{e}\nFallback to default.")
                _default_play(s["path"], vol)
        else:
            try:
                _default_play(s["path"], vol)
            except:
                _default_play(s["path"], 1.0)

    def _play_shortcut(self, key):
        fn = self.shortcuts.get(key)
        for i, s in enumerate(self.sounds):
            if s["filename"] == fn:
                return self.play(i)

if __name__ == "__main__":
    app = Soundboard()
    app.mainloop()
