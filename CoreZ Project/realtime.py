"""Real-time protection for CoreZ.

Watches one or more folders with watchdog and scans files as they are created
or modified. On an actionable detection it invokes a callback (the GUI shows an
alert / auto-quarantines). Degrades to a clear error if watchdog is missing.
"""

import os
import threading

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    _WATCHDOG_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    Observer = None
    FileSystemEventHandler = object
    _WATCHDOG_AVAILABLE = False

import scanner as _scanner


class _Handler(FileSystemEventHandler):
    def __init__(self, monitor):
        self._monitor = monitor

    def on_created(self, event):
        if not event.is_directory:
            self._monitor._queue(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self._monitor._queue(event.src_path)


class RealTimeProtection:
    """Start/stop a background watcher over a set of paths."""

    def __init__(self, scanner_obj=None, on_detection=None):
        self.scanner = scanner_obj or _scanner.default_scanner
        self.on_detection = on_detection  # callback(list[Detection])
        self._observer = None
        self._lock = threading.Lock()
        # debounce: avoid re-scanning the same path repeatedly on burst writes
        self._recent = {}

    @property
    def available(self):
        return _WATCHDOG_AVAILABLE

    @property
    def running(self):
        return self._observer is not None

    def _queue(self, path):
        # Run the scan off the watchdog thread pool via a short-lived thread so a
        # slow scan doesn't stall the observer.
        threading.Thread(target=self._scan_one, args=(path,), daemon=True).start()

    def _scan_one(self, path):
        try:
            if not os.path.isfile(path):
                return
            dets = self.scanner.scan_file(path)
        except (OSError, PermissionError):
            return
        actionable = [d for d in dets if d.actionable]
        if actionable and self.on_detection:
            self.on_detection(actionable)

    def start(self, paths):
        if not _WATCHDOG_AVAILABLE:
            raise RuntimeError("watchdog is not installed - real-time protection unavailable")
        with self._lock:
            if self._observer is not None:
                return
            observer = Observer()
            handler = _Handler(self)
            watched = 0
            for p in paths:
                if os.path.isdir(p):
                    observer.schedule(handler, p, recursive=True)
                    watched += 1
            if watched == 0:
                raise ValueError("no valid directories to watch")
            observer.start()
            self._observer = observer

    def stop(self):
        with self._lock:
            if self._observer is not None:
                self._observer.stop()
                self._observer.join(timeout=5)
                self._observer = None
