"""CoreZ Advance Security - tkinter dashboard.

Wires the dashboard buttons to the real engine: threaded scanning with a live
results table, a quarantine manager, real-time protection, junk cleaning,
settings and the RAM booster. Scans run on worker threads and report back to the
UI through a queue polled on the Tk main loop, so the window never freezes.
"""

import os
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import config
import engine
import junk as junk_mod
import scanner as scanner_mod
import signatures
from quarantine import default_quarantine
from realtime import RealTimeProtection

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(SCRIPT_DIR, "Images")

SEVERITY_COLORS = {
    "malicious": "#c0392b",
    "test": "#2980b9",
    "suspicious": "#e67e22",
}


def _img(name):
    """Load a PhotoImage if it exists, else return None (never crash on assets)."""
    path = os.path.join(IMG_DIR, name)
    if os.path.exists(path):
        try:
            return tk.PhotoImage(file=path)
        except tk.TclError:
            return None
    return None


class CoreZApp:
    def __init__(self, root):
        self.root = root
        self.cfg = config.load()
        self.scanner = scanner_mod.Scanner(
            use_yara=self.cfg.get("use_yara", True),
            use_heuristics=self.cfg.get("use_heuristics", True),
        )
        self.realtime = RealTimeProtection(self.scanner, on_detection=self._on_realtime_detection)
        self._rt_queue = queue.Queue()

        root.title("CoreZ Advance Security")
        root.geometry("900x600+220+65")
        root.resizable(0, 0)

        self._logo = _img("Logo.png")
        if self._logo:
            root.iconphoto(False, self._logo)

        self._bg = _img("Frame 1.png")
        if self._bg:
            tk.Label(root, image=self._bg).place(x=0, y=0, relwidth=1, relheight=1)
        else:
            root.configure(bg="#0b1e2d")

        self._build_buttons()
        self._poll_realtime_queue()

    # ---------------------------------------------------------------- layout
    def _build_buttons(self):
        style = ttk.Style()
        style.configure("Side.TButton", font=("Helvetica", 12))
        style.configure("Action.TButton", font=("Helvetica", 14))

        side = [
            ("Dashboard", self.root.lift),
            ("Protection", self.open_protection),
            ("Settings", self.open_settings),
            ("Quarantine", self.open_quarantine),
            ("Support", self.open_support),
        ]
        y = 150
        for text, cmd in side:
            ttk.Button(self.root, text=text, style="Side.TButton", command=cmd).place(x=40, y=y, width=150)
            y += 70

        actions = [
            ("Quick Scan", lambda: self.start_scan("quick"), 320, 200),
            ("Full Scan", lambda: self.start_scan("full"), 520, 280),
            ("Custom Scan", lambda: self.start_scan("custom"), 320, 360),
            ("Junk Cleaner", self.open_junk, 520, 440),
            ("RAM Booster", self.run_ramboost, 320, 520),
        ]
        for text, cmd, x, y in actions:
            ttk.Button(self.root, text=text, style="Action.TButton", command=cmd).place(x=x, y=y, width=170)

    # -------------------------------------------------------------- scanning
    def start_scan(self, mode):
        if mode == "custom":
            path = filedialog.askdirectory(title="Choose a folder to scan")
            if not path:
                return
            targets = [path]
            title = "Custom Scan"
        elif mode == "quick":
            targets = self._quick_targets()
            title = "Quick Scan"
        else:  # full
            targets = [os.path.expanduser("~")]
            title = "Full Scan"

        ScanWindow(self, targets, title)

    def _quick_targets(self):
        # High-risk, human-scale locations only - a "quick" scan must stay quick,
        # so we deliberately skip the system temp dir (often 100k+ files).
        home = os.path.expanduser("~")
        candidates = [
            os.path.join(home, "Downloads"),
            os.path.join(home, "Desktop"),
            os.path.join(home, "Documents"),
        ]
        return [c for c in candidates if os.path.isdir(c)] or [home]

    # --------------------------------------------------------- ram / junk
    def run_ramboost(self):
        win = tk.Toplevel(self.root)
        win.title("RAM Booster")
        win.geometry("460x180+360+220")
        lbl = tk.Label(win, text="Boosting RAM...", font=("Arial", 13))
        lbl.pack(pady=40)

        def work():
            try:
                out = engine.ramboost()
            except Exception as e:
                out = "RAM Booster failed: {}".format(e)
            self.root.after(0, lambda: lbl.config(text=out))
        threading.Thread(target=work, daemon=True).start()

    def open_junk(self):
        JunkWindow(self)

    # --------------------------------------------------------- quarantine
    def open_quarantine(self):
        QuarantineWindow(self)

    # --------------------------------------------------------- protection
    def open_protection(self):
        ProtectionWindow(self)

    def _on_realtime_detection(self, detections):
        # Runs on a watchdog worker thread - hand off to the UI thread via queue.
        self._rt_queue.put(detections)

    def _poll_realtime_queue(self):
        try:
            while True:
                detections = self._rt_queue.get_nowait()
                self._handle_realtime_detections(detections)
        except queue.Empty:
            pass
        self.root.after(400, self._poll_realtime_queue)

    def _handle_realtime_detections(self, detections):
        names = "\n".join("- {} ({})".format(os.path.basename(d.path), d.name) for d in detections)
        auto = self.cfg.get("auto_quarantine_realtime", True)
        if auto:
            for d in detections:
                try:
                    default_quarantine.quarantine(d.path, d.name, d.severity)
                except OSError:
                    pass
            messagebox.showwarning(
                "CoreZ - Threat quarantined",
                "Real-time protection quarantined:\n\n{}".format(names),
            )
        else:
            messagebox.showwarning(
                "CoreZ - Threat detected",
                "Real-time protection found:\n\n{}".format(names),
            )

    # --------------------------------------------------------- settings
    def open_settings(self):
        SettingsWindow(self)

    def open_support(self):
        win = tk.Toplevel(self.root)
        win.title("Support")
        win.geometry("520x300+360+180")
        msg = (
            "CoreZ Advance Security\n\n"
            "A Python antivirus: MD5 signature scanning, YARA rules, heuristics,\n"
            "quarantine, real-time protection and system cleanup.\n\n"
            "Signature database: {:,} known-malware hashes.\n\n"
            "Test detection safely with the EICAR test file:\n"
            "https://www.eicar.org/download-anti-malware-testfile/"
        ).format(len(signatures.default_db))
        tk.Label(win, text=msg, font=("Arial", 11), justify="left").pack(padx=20, pady=20)


class ScanWindow:
    """A scan session: progress + live results + quarantine actions."""

    def __init__(self, app, targets, title):
        self.app = app
        self.targets = targets
        self.cancel_event = threading.Event()
        self.queue = queue.Queue()
        self.detections_by_item = {}

        self.win = tk.Toplevel(app.root)
        self.win.title(title)
        self.win.geometry("820x560+240+90")
        self.win.protocol("WM_DELETE_WINDOW", self._on_close)

        top = tk.Frame(self.win)
        top.pack(fill="x", padx=12, pady=8)
        tk.Label(top, text=title, font=("Arial", 15, "bold")).pack(anchor="w")
        self.status = tk.Label(top, text="Starting...", font=("Arial", 10), anchor="w")
        self.status.pack(fill="x")
        self.progress = ttk.Progressbar(top, mode="indeterminate")
        self.progress.pack(fill="x", pady=4)
        self.progress.start(12)

        cols = ("severity", "type", "detection", "file")
        self.tree = ttk.Treeview(self.win, columns=cols, show="headings", height=16)
        for c, w in zip(cols, (90, 90, 240, 360)):
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=w, anchor="w")
        for sev, color in SEVERITY_COLORS.items():
            self.tree.tag_configure(sev, foreground=color)
        self.tree.pack(fill="both", expand=True, padx=12, pady=6)

        btns = tk.Frame(self.win)
        btns.pack(fill="x", padx=12, pady=8)
        self.quarantine_btn = ttk.Button(btns, text="Quarantine selected", command=self._quarantine_selected, state="disabled")
        self.quarantine_btn.pack(side="left")
        self.quarantine_all_btn = ttk.Button(btns, text="Quarantine all threats", command=self._quarantine_all, state="disabled")
        self.quarantine_all_btn.pack(side="left", padx=6)
        self.cancel_btn = ttk.Button(btns, text="Cancel", command=self._cancel)
        self.cancel_btn.pack(side="right")

        self.worker = threading.Thread(target=self._run, daemon=True)
        self.worker.start()
        self.win.after(100, self._poll)

    def _run(self):
        def progress(path, count, detection):
            self.queue.put(("progress", path, count, detection))
        try:
            result = self.app.scanner.scan(self.targets, progress=progress, cancel=self.cancel_event)
            self.queue.put(("done", result))
        except Exception as e:  # defensive - keep the UI alive
            self.queue.put(("error", str(e)))

    def _poll(self):
        try:
            while True:
                msg = self.queue.get_nowait()
                kind = msg[0]
                if kind == "progress":
                    _, path, count, detection = msg
                    self.status.config(text="Scanned {} files - {}".format(count, path[:80]))
                    if detection is not None:
                        self._add_detection(detection)
                elif kind == "done":
                    self._finish(msg[1])
                    return
                elif kind == "error":
                    self.progress.stop()
                    self.status.config(text="Scan error: {}".format(msg[1]))
                    return
        except queue.Empty:
            pass
        self.win.after(100, self._poll)

    def _add_detection(self, d):
        item = self.tree.insert(
            "", "end",
            values=(d.severity, d.method, d.name, d.path),
            tags=(d.severity,),
        )
        self.detections_by_item[item] = d
        if any(x.actionable for x in self.detections_by_item.values()):
            self.quarantine_all_btn.config(state="normal")
        self.quarantine_btn.config(state="normal")

    def _finish(self, result):
        self.progress.stop()
        self.progress.config(mode="determinate", value=100)
        threats = len(result.threats)
        total = len(result.detections)
        suffix = " (cancelled)" if result.cancelled else ""
        self.status.config(text=(
            "Done{}. {} files scanned in {:.1f}s - {} threat(s), {} total finding(s).".format(
                suffix, result.files_scanned, result.duration, threats, total)
        ))
        self.cancel_btn.config(text="Close", command=self.win.destroy)
        if total == 0:
            messagebox.showinfo("CoreZ", "No threats found. You're clean!", parent=self.win)

    def _cancel(self):
        self.cancel_event.set()
        self.status.config(text="Cancelling...")

    def _on_close(self):
        self.cancel_event.set()
        self.win.destroy()

    def _quarantine_items(self, items):
        done, failed = 0, 0
        for item in items:
            d = self.detections_by_item.get(item)
            if d is None:
                continue
            try:
                default_quarantine.quarantine(d.path, d.name, d.severity)
                self.tree.item(item, values=(d.severity, d.method, d.name, d.path + "  [quarantined]"))
                done += 1
            except OSError:
                failed += 1
        messagebox.showinfo(
            "Quarantine",
            "Quarantined {} file(s).{}".format(done, "" if not failed else " {} failed.".format(failed)),
            parent=self.win,
        )

    def _quarantine_selected(self):
        self._quarantine_items(self.tree.selection())

    def _quarantine_all(self):
        items = [i for i, d in self.detections_by_item.items() if d.actionable]
        self._quarantine_items(items)


class QuarantineWindow:
    def __init__(self, app):
        self.app = app
        self.win = tk.Toplevel(app.root)
        self.win.title("Quarantine Vault")
        self.win.geometry("760x460+280+120")

        tk.Label(self.win, text="Quarantined items", font=("Arial", 14, "bold")).pack(anchor="w", padx=12, pady=8)
        cols = ("detection", "severity", "original_path", "quarantined_at")
        self.tree = ttk.Treeview(self.win, columns=cols, show="headings", height=15)
        for c, w in zip(cols, (200, 90, 330, 130)):
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=12, pady=6)
        self.id_by_item = {}

        btns = tk.Frame(self.win)
        btns.pack(fill="x", padx=12, pady=8)
        ttk.Button(btns, text="Restore", command=self._restore).pack(side="left")
        ttk.Button(btns, text="Delete permanently", command=self._delete).pack(side="left", padx=6)
        ttk.Button(btns, text="Refresh", command=self._refresh).pack(side="left")
        ttk.Button(btns, text="Close", command=self.win.destroy).pack(side="right")

        self._refresh()

    def _refresh(self):
        self.tree.delete(*self.tree.get_children())
        self.id_by_item.clear()
        for e in default_quarantine.list_entries():
            item = self.tree.insert("", "end", values=(
                e.get("detection", ""), e.get("severity", ""),
                e.get("original_path", ""), e.get("quarantined_at", ""),
            ))
            self.id_by_item[item] = e["id"]

    def _selected_ids(self):
        return [self.id_by_item[i] for i in self.tree.selection() if i in self.id_by_item]

    def _restore(self):
        ids = self._selected_ids()
        if not ids:
            return
        if not messagebox.askyesno("Restore", "Restore {} file(s) to their original location?".format(len(ids)), parent=self.win):
            return
        for qid in ids:
            try:
                default_quarantine.restore(qid)
            except (OSError, KeyError) as e:
                messagebox.showerror("Restore failed", str(e), parent=self.win)
        self._refresh()

    def _delete(self):
        ids = self._selected_ids()
        if not ids:
            return
        if not messagebox.askyesno("Delete", "Permanently delete {} file(s)? This cannot be undone.".format(len(ids)), parent=self.win):
            return
        for qid in ids:
            try:
                default_quarantine.delete(qid)
            except KeyError:
                pass
        self._refresh()


class ProtectionWindow:
    def __init__(self, app):
        self.app = app
        self.win = tk.Toplevel(app.root)
        self.win.title("Real-Time Protection")
        self.win.geometry("560x360+320+140")

        tk.Label(self.win, text="Real-Time Protection", font=("Arial", 15, "bold")).pack(anchor="w", padx=16, pady=10)

        if not app.realtime.available:
            tk.Label(self.win, text="watchdog is not installed - real-time protection unavailable.\nRun: pip install watchdog",
                     fg="#c0392b", font=("Arial", 11), justify="left").pack(padx=16, pady=10)
            return

        self.paths = list(app.cfg.get("realtime_paths", []))
        tk.Label(self.win, text="Watched folders:", font=("Arial", 11)).pack(anchor="w", padx=16)
        self.listbox = tk.Listbox(self.win, height=5)
        self.listbox.pack(fill="x", padx=16)
        for p in self.paths:
            self.listbox.insert("end", p)

        path_btns = tk.Frame(self.win)
        path_btns.pack(fill="x", padx=16, pady=4)
        ttk.Button(path_btns, text="Add folder", command=self._add).pack(side="left")
        ttk.Button(path_btns, text="Remove selected", command=self._remove).pack(side="left", padx=6)

        self.status = tk.Label(self.win, text="", font=("Arial", 11))
        self.status.pack(anchor="w", padx=16, pady=8)

        self.toggle_btn = ttk.Button(self.win, text="", command=self._toggle)
        self.toggle_btn.pack(padx=16, pady=6)
        self._update_state()

    def _update_state(self):
        running = self.app.realtime.running
        self.status.config(
            text="Status: {}".format("PROTECTED - monitoring active" if running else "OFF"),
            fg="#27ae60" if running else "#c0392b",
        )
        self.toggle_btn.config(text="Turn Off" if running else "Turn On")

    def _add(self):
        path = filedialog.askdirectory(title="Add folder to monitor", parent=self.win)
        if path and path not in self.paths:
            self.paths.append(path)
            self.listbox.insert("end", path)

    def _remove(self):
        for i in reversed(self.listbox.curselection()):
            del self.paths[i]
            self.listbox.delete(i)

    def _toggle(self):
        if self.app.realtime.running:
            self.app.realtime.stop()
        else:
            valid = [p for p in self.paths if os.path.isdir(p)]
            if not valid:
                messagebox.showerror("Protection", "Add at least one valid folder to monitor.", parent=self.win)
                return
            try:
                self.app.realtime.start(valid)
            except (RuntimeError, ValueError) as e:
                messagebox.showerror("Protection", str(e), parent=self.win)
                return
            self.app.cfg["realtime_paths"] = self.paths
            config.save(self.app.cfg)
        self._update_state()


class JunkWindow:
    def __init__(self, app):
        self.app = app
        self.win = tk.Toplevel(app.root)
        self.win.title("Junk Cleaner")
        self.win.geometry("620x420+320+140")

        tk.Label(self.win, text="Junk Cleaner", font=("Arial", 15, "bold")).pack(anchor="w", padx=16, pady=10)
        self.summary = tk.Label(self.win, text="Scanning temp locations...", font=("Arial", 11), justify="left")
        self.summary.pack(anchor="w", padx=16)

        self.text = tk.Text(self.win, height=12, width=70)
        self.text.pack(fill="both", expand=True, padx=16, pady=8)

        btns = tk.Frame(self.win)
        btns.pack(fill="x", padx=16, pady=8)
        self.clean_btn = ttk.Button(btns, text="Clean now", command=self._clean, state="disabled")
        self.clean_btn.pack(side="left")
        ttk.Button(btns, text="Rescan", command=self._scan).pack(side="left", padx=6)
        ttk.Button(btns, text="Close", command=self.win.destroy).pack(side="right")

        self._scan()

    def _scan(self):
        self.clean_btn.config(state="disabled")
        self.text.delete("1.0", "end")
        self.summary.config(text="Scanning temp locations...")

        def work():
            total, count, per_dir = junk_mod.scan_junk()
            self.win.after(0, lambda: self._show(total, count, per_dir))
        threading.Thread(target=work, daemon=True).start()

    def _show(self, total, count, per_dir):
        self.summary.config(text="Found {} in {} files across {} locations.".format(
            junk_mod.human_size(total), count, len(per_dir)))
        self.text.delete("1.0", "end")
        for d, b, c in per_dir:
            self.text.insert("end", "{:>10}  {:>6} files  {}\n".format(junk_mod.human_size(b), c, d))
        self.clean_btn.config(state="normal" if count else "disabled")

    def _clean(self):
        if not messagebox.askyesno("Junk Cleaner", "Delete temporary files now?", parent=self.win):
            return

        def work():
            freed, removed, errors = junk_mod.clean_junk()
            msg = "Freed {} - removed {} files ({} skipped/in use).".format(
                junk_mod.human_size(freed), removed, errors)
            self.win.after(0, lambda: (self.summary.config(text=msg), self._scan()))
        threading.Thread(target=work, daemon=True).start()


class SettingsWindow:
    def __init__(self, app):
        self.app = app
        self.win = tk.Toplevel(app.root)
        self.win.title("Settings")
        self.win.geometry("560x400+320+140")
        cfg = app.cfg

        tk.Label(self.win, text="Settings", font=("Arial", 15, "bold")).pack(anchor="w", padx=16, pady=10)

        self.use_yara = tk.BooleanVar(value=cfg.get("use_yara", True))
        self.use_heur = tk.BooleanVar(value=cfg.get("use_heuristics", True))
        self.auto_q = tk.BooleanVar(value=cfg.get("auto_quarantine_realtime", True))
        ttk.Checkbutton(self.win, text="Enable YARA rule scanning", variable=self.use_yara).pack(anchor="w", padx=20, pady=3)
        ttk.Checkbutton(self.win, text="Enable heuristic analysis", variable=self.use_heur).pack(anchor="w", padx=20, pady=3)
        ttk.Checkbutton(self.win, text="Auto-quarantine real-time detections", variable=self.auto_q).pack(anchor="w", padx=20, pady=3)

        tk.Label(self.win, text="VirusTotal API key (optional):", font=("Arial", 11)).pack(anchor="w", padx=20, pady=(16, 2))
        self.vt_key = tk.Entry(self.win, width=60, show="*")
        self.vt_key.insert(0, cfg.get("vt_api_key", ""))
        self.vt_key.pack(anchor="w", padx=20)
        tk.Label(self.win, text="(or set the CoreZ_VT_API_KEY environment variable)",
                 font=("Arial", 9), fg="#888").pack(anchor="w", padx=20)

        tk.Label(self.win, text="Signature DB: {:,} hashes loaded".format(len(signatures.default_db)),
                 font=("Arial", 10)).pack(anchor="w", padx=20, pady=(16, 2))

        btns = tk.Frame(self.win)
        btns.pack(fill="x", padx=16, pady=16)
        ttk.Button(btns, text="Save", command=self._save).pack(side="left")
        ttk.Button(btns, text="Close", command=self.win.destroy).pack(side="right")

    def _save(self):
        cfg = self.app.cfg
        cfg["use_yara"] = self.use_yara.get()
        cfg["use_heuristics"] = self.use_heur.get()
        cfg["auto_quarantine_realtime"] = self.auto_q.get()
        cfg["vt_api_key"] = self.vt_key.get().strip()
        config.save(cfg)
        # apply scan-layer toggles immediately
        self.app.scanner.use_yara = cfg["use_yara"]
        self.app.scanner.use_heuristics = cfg["use_heuristics"]
        messagebox.showinfo("Settings", "Saved.", parent=self.win)


def main():
    root = tk.Tk()
    CoreZApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
