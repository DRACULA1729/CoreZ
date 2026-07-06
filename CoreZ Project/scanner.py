"""Scan orchestration for CoreZ.

Combines three detection layers over each file:
  1. MD5 signature blacklist  (signatures.SignatureDB)   -> "malicious"
  2. YARA pattern rules        (yara_scanner.YaraScanner)  -> rule-defined severity
  3. Heuristics                (heuristics.analyze)        -> "suspicious"

Designed to run on a worker thread: pass a ``progress`` callback for UI updates
and a ``threading.Event`` as ``cancel`` to stop early.
"""

import os
import time
from dataclasses import dataclass, field

import heuristics
import signatures
import yara_scanner

# Severities that warrant remediation (quarantine), vs advisory-only.
ACTIONABLE = {"malicious", "test"}

# Directories skipped during a walk: dev/package noise, caches, and CoreZ's own
# vault. Pruning these keeps a Full Scan tractable instead of walking 100k+ cache
# files. Malware living in these is out of scope for a hash/YARA sweep anyway.
SKIP_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv", "env", ".env",
    "site-packages", ".cache", ".cargo", ".npm", ".rustup", ".gradle", ".m2",
    "quarantine_vault", "snap", ".local/share/Trash", ".mozilla", ".config/google-chrome",
    "proc", "sys", "dev", "run",
}


@dataclass
class Detection:
    path: str
    method: str          # "signature" | "yara" | "heuristic"
    name: str            # malware/rule name or heuristic reason
    severity: str        # "malicious" | "suspicious" | "test"

    @property
    def actionable(self):
        return self.severity in ACTIONABLE


@dataclass
class ScanResult:
    files_scanned: int = 0
    bytes_scanned: int = 0
    detections: list = field(default_factory=list)
    errors: list = field(default_factory=list)   # (path, message)
    duration: float = 0.0
    cancelled: bool = False

    @property
    def threats(self):
        return [d for d in self.detections if d.actionable]


class Scanner:
    def __init__(self, sig_db=None, yara=None, use_yara=True, use_heuristics=True):
        self.sig_db = sig_db or signatures.default_db
        self.yara = yara or yara_scanner.default_scanner
        self.use_yara = use_yara
        self.use_heuristics = use_heuristics

    # -- file enumeration ---------------------------------------------------
    def _iter_files(self, targets):
        for target in targets:
            if os.path.isfile(target):
                yield target
            elif os.path.isdir(target):
                # topdown so we can prune noise dirs in place; don't follow
                # symlinks (avoids loops and escaping the scan root).
                for dirpath, dirs, filenames in os.walk(target, followlinks=False):
                    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                    for fn in filenames:
                        yield os.path.join(dirpath, fn)

    # -- single-file scan ---------------------------------------------------
    def scan_file(self, path):
        """Return a list of Detection objects for one file."""
        found = []

        # 1. signature (also gives us the MD5 for free via the DB match)
        try:
            name = self.sig_db.match(path)
        except OSError as e:
            raise e
        if name:
            found.append(Detection(path, "signature", name, "malicious"))

        # 2. YARA
        if self.use_yara:
            for rule, desc, severity in self.yara.match(path):
                found.append(Detection(path, "yara", desc or rule, severity))

        # 3. heuristics
        if self.use_heuristics:
            for reason in heuristics.analyze(path):
                found.append(Detection(path, "heuristic", reason, "suspicious"))

        return found

    # -- directory / multi-target scan -------------------------------------
    def scan(self, targets, progress=None, cancel=None):
        """Scan files/dirs. ``progress(current_path, files_done, detection_or_None)``
        is called per file; ``cancel`` is a threading.Event checked between files.
        """
        if isinstance(targets, (str, os.PathLike)):
            targets = [targets]

        result = ScanResult()
        start = time.monotonic()

        for path in self._iter_files(targets):
            if cancel is not None and cancel.is_set():
                result.cancelled = True
                break
            try:
                dets = self.scan_file(path)
                try:
                    result.bytes_scanned += os.path.getsize(path)
                except OSError:
                    pass
            except (OSError, PermissionError) as e:
                result.errors.append((path, str(e)))
                dets = []
            result.files_scanned += 1
            for d in dets:
                result.detections.append(d)
            if progress is not None:
                progress(path, result.files_scanned, dets[0] if dets else None)

        result.duration = time.monotonic() - start
        return result


default_scanner = Scanner()
