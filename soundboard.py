import os, json, shutil, math
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox

# ─── Playback backends ────────────────────────────────────────────────────────
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

# ─── sounddevice for routing & mic meter ─────────────────────────────────────
try:
    import sounddevice as sd
    import soundfile as sf
    SD_AVAILABLE = True
except ImportError:
    SD_AVAILABLE = False
    print("⚠️  Install 'sounddevice' + 'soundfile' for routing & mic meter.")

# ─── Global hotkeys ───────────────────────────────────────────────────────────
try:
    import keyboard
    GLOBAL_HOTKEYS = True
except ImportError:
    GLOBAL_HOTKEYS = False
    print("⚠️  Install 'keyboard' if you want Ctrl+number globally.")

# ─── Constants ────────────────────────────────────────────────────────────────
SAVEDIR     = os.path.join(os.getcwd(), "SavedSounds")
CONFIG_PATH = os.path.join(SAVEDIR, "config.json")
AUDIO_EXTS  = {".wav", ".mp3", ".ogg", ".flac"}


class Soundboard(tk.Tk):
    SHORTCUT_KEYS = list("1234567890")

    def __init__(self):
        super().__init__()
        self.title("Soundboard")
        self.geometry("750x900")

        # ─── Enumerate audio devices BEFORE loading config ────────────────
        if SD_AVAILABLE:
            all_devs = sd.query_devices()
            self.device_options_output = [
                d["name"] for d in all_devs if d["max_output_channels"] > 0
            ]
            self.device_map_output = {
                d["name"]: i for i, d in enumerate(all_devs) if d["max_output_channels"] > 0
            }
            self.device_options_input = [
                d["name"] for d in all_devs if d["max_input_channels"] > 0
            ]
            self.device_map_input = {
                d["name"]: i for i, d in enumerate(all_devs) if d["max_input_channels"] > 0
            }
        else:
            self.device_options_output = []
            self.device_map_output    = {}
            self.device_options_input = []
            self.device_map_input     = {}

        # ─── State vars ──────────────────────────────────────────────────────
        self.sounds        = []  # {"filename","name","path"}
        self.shortcuts     = {}  # key→filename
        self.use_mic_var   = tk.BooleanVar()
        self.route_dev_var = tk.StringVar()
        self.play_vol_var  = tk.DoubleVar()
        self.mic_in_var    = tk.StringVar()
        self.mic_level_var = tk.DoubleVar(value=0.0)

        # ─── Load or create SavedSounds + config ────────────────────────────
        os.makedirs(SAVEDIR, exist_ok=True)
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        else:
            cfg = {
                "sounds": [], "shortcuts": {},
                "use_mic": False, "route_device": None,
                "play_volume": 100.0, "mic_input_device": None
            }

        # populate sounds list
        name_map = {s["filename"]: s["name"] for s in cfg.get("sounds", [])}
        files    = sorted(
            fn for fn in os.listdir(SAVEDIR)
            if os.path.splitext(fn)[1].lower() in AUDIO_EXTS
        )
        for fn in files:
            self.sounds.append({
                "filename": fn,
                "name":     name_map.get(fn, os.path.splitext(fn)[0]),
                "path":     os.path.join(SAVEDIR, fn)
            })

        # populate shortcuts
        self.shortcuts = {
            k: v for k, v in cfg.get("shortcuts", {}).items()
            if k in self.SHORTCUT_KEYS and v in files
        }

        # load settings
        self.use_mic_var.set(cfg.get("use_mic", False))
        self.route_dev_var.set(
            cfg.get("route_device") if cfg.get("route_device") in self.device_options_output
            else (self.device_options_output[0] if self.device_options_output else "")
        )
        self.play_vol_var.set(cfg.get("play_volume", 100.0))
        self.mic_in_var.set(
            cfg.get("mic_input_device") if cfg.get("mic_input_device") in self.device_options_input
            else (self.device_options_input[0] if self.device_options_input else "")
        )

        # ensure config file exists/updated
        self._save_config()

        # ─── Build UI ────────────────────────────────────────────────────────
        self._build_settings_frame()
        self._build_shortcut_frame()
        self._build_control_frame()
        self._build_list_frame()

        # ─── Global hotkeys ────────────────────────────────────────────────
        if GLOBAL_HOTKEYS:
            for k in self.SHORTCUT_KEYS:
                keyboard.add_hotkey(f"ctrl+{k}",
                                    lambda k=k: self._play_shortcut(k))

        # ─── Mic input meter ───────────────────────────────────────────────
        if SD_AVAILABLE and self.device_options_input:
            try:
                inp_idx = self.device_map_input[self.mic_in_var.get()]
                self._mic_stream = sd.InputStream(
                    device=inp_idx, channels=1, callback=self._mic_cb
                )
                self._mic_stream.start()
            except Exception as e:
                print("Mic meter start error:", e)

        self.focus_set()

    def _save_config(self):
        data = {
            "sounds": [
                {"filename": s["filename"], "name": s["name"]}
                for s in self.sounds
            ],
            "shortcuts":        self.shortcuts,
            "use_mic":          self.use_mic_var.get(),
            "route_device":     self.route_dev_var.get(),
            "play_volume":      self.play_vol_var.get(),
            "mic_input_device": self.mic_in_var.get()
        }
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # ─── UI Sections ──────────────────────────────────────────────────────────
    def _build_settings_frame(self):
        frm = ttk.LabelFrame(self, text="Settings & Test Meters")
        frm.pack(fill="x", padx=10, pady=10)

        # Speaker / routing device
        if self.device_options_output:
            ttk.Label(frm, text="Route Output → Mic device:")\
               .grid(row=0, column=0, sticky="w")
            out = ttk.Combobox(frm,
                values=self.device_options_output,
                textvariable=self.route_dev_var,
                state="readonly", width=30
            )
            out.grid(row=0, column=1, padx=5, sticky="w")
            out.bind("<<ComboboxSelected>>", lambda e: self._save_config())

        # playback volume slider
        ttk.Label(frm, text="Playback Volume:")\
           .grid(row=1, column=0, sticky="w")
        vol = ttk.Scale(frm, from_=0, to=100, variable=self.play_vol_var,
                        orient="horizontal", command=lambda e: self._save_config())
        vol.grid(row=1, column=1, padx=5, sticky="ew")

        # mic input selector
        if self.device_options_input:
            ttk.Label(frm, text="Mic Input Device:")\
               .grid(row=2, column=0, sticky="w")
            mic = ttk.Combobox(frm,
                values=self.device_options_input,
                textvariable=self.mic_in_var,
                state="readonly", width=30
            )
            mic.grid(row=2, column=1, padx=5, sticky="w")
            mic.bind("<<ComboboxSelected>>",
                     lambda e: [self._save_config(), self._restart_mic_stream()])

        # mic level meter
        ttk.Label(frm, text="Mic Level:")\
           .grid(row=3, column=0, sticky="w")
        pb = ttk.Progressbar(frm, orient="horizontal", maximum=100,
                             variable=self.mic_level_var)
        pb.grid(row=3, column=1, padx=5, sticky="ew")

        frm.columnconfigure(1, weight=1)

    def _build_shortcut_frame(self):
        frm = ttk.LabelFrame(self, text="Quick-Access Shortcuts (Ctrl+1…0)")
        frm.pack(fill="x", padx=10, pady=10)
        self.shortcut_buttons = {}
        for i, k in enumerate(self.SHORTCUT_KEYS):
            btn = ttk.Button(frm, text=f"{k}: ---",
                command=lambda k=k: self._play_shortcut(k))
            btn.grid(row=0, column=i, padx=2, pady=5, sticky="ew")
            frm.columnconfigure(i, weight=1)
            self.shortcut_buttons[k] = btn
        self._refresh_shortcuts()

    def _build_control_frame(self):
        frm = ttk.Frame(self)
        frm.pack(fill="x", padx=10, pady=(0,10))
        ttk.Checkbutton(frm, text="Route to Microphone",
            variable=self.use_mic_var, command=self._save_config)\
            .pack(side="left")
        ttk.Button(frm, text="➕ Load Sound", command=self.load_sound)\
            .pack(side="left", padx=5)

    def _build_list_frame(self):
        lf = ttk.LabelFrame(self, text="All Loaded Sounds")
        lf.pack(fill="both", expand=True, padx=10, pady=(0,10))
        canvas = tk.Canvas(lf)
        scroll = ttk.Scrollbar(lf, orient="vertical", command=canvas.yview)
        self.inner = ttk.Frame(canvas)
        self.inner.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0,0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.update_list()

    # ─── Mic stream & callback ───────────────────────────────────────────────
    def _mic_cb(self, indata, frames, time, status):
        # compute RMS on channel 0 without numpy
        total = 0.0
        count = 0
        for samp in indata:
            total += samp[0] * samp[0]
            count += 1
        if count:
            rms = math.sqrt(total / count)
            level = min(rms * 300, 100)
            self.mic_level_var.set(level)

    def _restart_mic_stream(self):
        if hasattr(self, "_mic_stream"):
            try:
                self._mic_stream.stop()
                self._mic_stream.close()
            except:
                pass
        try:
            idx = self.device_map_input[self.mic_in_var.get()]
            self._mic_stream = sd.InputStream(
                device=idx, channels=1, callback=self._mic_cb
            )
            self._mic_stream.start()
        except Exception as e:
            messagebox.showerror("Mic Error", f"Could not open mic:\n{e}")

    # ─── Soundboard logic ────────────────────────────────────────────────────
    def load_sound(self):
        if len(self.sounds) >= 100:
            return messagebox.showwarning("Limit reached","Max 100 sounds.")
        path = filedialog.askopenfilename(
            filetypes=[("Audio","*.wav *.mp3 *.ogg *.flac")]
        )
        if not path: return
        name = simpledialog.askstring("Name","Enter display name:") or os.path.basename(path)
        fn, ext = os.path.basename(path), ""
        base, ext = os.path.splitext(fn)
        dest = os.path.join(SAVEDIR, fn); i=1
        while os.path.exists(dest):
            fn = f"{base}({i}){ext}"
            dest = os.path.join(SAVEDIR, fn); i+=1
        shutil.copy2(path, dest)
        self.sounds.append({"filename":fn,"name":name,"path":dest})
        self._save_config(); self.update_list(); self._refresh_shortcuts()

    def update_list(self):
        for w in self.inner.winfo_children():
            w.destroy()
        for i, s in enumerate(self.sounds):
            ttk.Label(self.inner, text=s["name"], width=30)\
               .grid(row=i,column=0,padx=5,pady=2,sticky="w")
            ttk.Button(self.inner,text="▶ Play",command=lambda i=i:self.play(i))\
               .grid(row=i,column=1,padx=5,pady=2)
            ttk.Button(self.inner,text="🔑 Assign",command=lambda i=i:self.assign(i))\
               .grid(row=i,column=2,padx=5,pady=2)
            ttk.Button(self.inner,text="🗑 Delete",command=lambda i=i:self.delete(i))\
               .grid(row=i,column=3,padx=5,pady=2)

    def delete(self, idx):
        s = self.sounds[idx]
        if not messagebox.askyesno("Delete",f"Remove '{s['name']}'?"): return
        try:
            os.remove(s["path"])
        except OSError as e:
            return messagebox.showerror("Err",e)
        fn=s["filename"]; self.sounds.pop(idx)
        self.shortcuts={k:v for k,v in self.shortcuts.items() if v!=fn}
        self._save_config(); self.update_list(); self._refresh_shortcuts()

    def assign(self, idx):
        key = simpledialog.askstring("Assign","Slot (1–9 or 0):")
        if key not in self.SHORTCUT_KEYS:
            return messagebox.showerror("Invalid","Must be 1–9 or 0.")
        self.shortcuts[key]=self.sounds[idx]["filename"]
        self._save_config(); self._refresh_shortcuts()

    def _refresh_shortcuts(self):
        for k, btn in self.shortcut_buttons.items():
            fn = self.shortcuts.get(k)
            nm = next((s["name"] for s in self.sounds if s["filename"]==fn),"---")
            btn.config(text=f"{k}: {nm}")

    def play(self, idx):
        s = self.sounds[idx]
        vol = float(self.play_vol_var.get())/100.0
        if self.use_mic_var.get() and SD_AVAILABLE and self.route_dev_var.get():
            data, fs = sf.read(s["path"], dtype="float32")
            data *= vol
            dev = self.device_map_output.get(self.route_dev_var.get())
            sd.play(data, fs, device=dev)
        else:
            try:
                _default_play(s["path"], vol)
            except:
                _default_play(s["path"], 1.0)

    def _play_shortcut(self, key):
        fn = self.shortcuts.get(key)
        for i,s in enumerate(self.sounds):
            if s["filename"]==fn:
                return self.play(i)


if __name__ == "__main__":
    app = Soundboard()
    app.mainloop()
