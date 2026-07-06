"""Lightweight, signature-free heuristics for CoreZ.

These are cheap checks that flag *suspicious* files the hash blacklist and YARA
rules might miss. They are intentionally conservative and return advisory
findings (severity "suspicious"), never hard verdicts, to keep false positives
from auto-quarantining a user's files.
"""

import math
import os

# Executable / script extensions that are worth extra scrutiny.
EXECUTABLE_EXTS = {
    ".exe", ".dll", ".scr", ".com", ".bat", ".cmd", ".ps1", ".vbs", ".js",
    ".jar", ".msi", ".sh", ".bin", ".elf", ".apk",
}

# Extensions commonly abused in "double extension" tricks (photo.jpg.exe).
DECOY_EXTS = {
    ".jpg", ".jpeg", ".png", ".gif", ".pdf", ".doc", ".docx", ".xls",
    ".xlsx", ".txt", ".mp3", ".mp4", ".zip",
}

# Files above this size skip the entropy read (too big to be worth it).
_MAX_ENTROPY_BYTES = 8 * 1024 * 1024


def shannon_entropy(data):
    """Shannon entropy (bits/byte, 0-8) of a bytes buffer."""
    if not data:
        return 0.0
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    entropy = 0.0
    length = len(data)
    for c in counts:
        if c:
            p = c / length
            entropy -= p * math.log2(p)
    return entropy


def _double_extension(name):
    """Return the decoy+executable pair if the name uses a double extension."""
    parts = name.lower().rsplit(".", 2)
    if len(parts) == 3:
        _, mid, last = parts
        if "." + mid in DECOY_EXTS and "." + last in EXECUTABLE_EXTS:
            return mid, last
    return None


def analyze(path):
    """Return a list of heuristic reason strings for a file (empty if clean)."""
    reasons = []
    name = os.path.basename(path)
    _, ext = os.path.splitext(name.lower())

    double = _double_extension(name)
    if double:
        reasons.append(
            "Double extension (.{}.{}) disguising an executable".format(*double)
        )

    try:
        size = os.path.getsize(path)
    except OSError:
        return reasons

    # High-entropy executables are often packed/encrypted (common in malware).
    if ext in EXECUTABLE_EXTS and 0 < size <= _MAX_ENTROPY_BYTES:
        try:
            with open(path, "rb") as f:
                data = f.read(_MAX_ENTROPY_BYTES)
        except OSError:
            return reasons
        ent = shannon_entropy(data)
        if ent >= 7.2:
            reasons.append(
                "High entropy ({:.2f} bits/byte) executable - likely packed/encrypted".format(ent)
            )

    return reasons
