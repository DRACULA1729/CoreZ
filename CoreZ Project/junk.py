"""Junk / temp file cleaner for CoreZ.

Scans well-known temporary/cache locations, reports what could be freed, and
deletes on request. Cross-platform. Always preview before cleaning; we skip
files currently in use and never touch anything outside the known temp roots.
"""

import os
import shutil
import tempfile


def _candidate_dirs():
    dirs = []
    # System + user temp
    dirs.append(tempfile.gettempdir())

    if os.name == "nt":
        for env in ("TEMP", "TMP"):
            v = os.environ.get(env)
            if v:
                dirs.append(v)
        local = os.environ.get("LOCALAPPDATA")
        if local:
            dirs.append(os.path.join(local, "Temp"))
    else:
        home = os.path.expanduser("~")
        dirs.append(os.path.join(home, ".cache"))
        dirs.append("/var/tmp")

    # de-dup while preserving order, keep only existing dirs
    seen, out = set(), []
    for d in dirs:
        d = os.path.abspath(d)
        if d not in seen and os.path.isdir(d):
            seen.add(d)
            out.append(d)
    return out


def scan_junk():
    """Return (total_bytes, file_count, per_dir_summary) without deleting."""
    total = 0
    count = 0
    summary = []
    for d in _candidate_dirs():
        d_bytes = 0
        d_count = 0
        for dirpath, _dirs, filenames in os.walk(d):
            for fn in filenames:
                fp = os.path.join(dirpath, fn)
                try:
                    d_bytes += os.path.getsize(fp)
                    d_count += 1
                except OSError:
                    continue
        summary.append((d, d_bytes, d_count))
        total += d_bytes
        count += d_count
    return total, count, summary


def clean_junk():
    """Delete junk files. Returns (bytes_freed, files_removed, errors)."""
    freed = 0
    removed = 0
    errors = 0
    for d in _candidate_dirs():
        for dirpath, _dirs, filenames in os.walk(d):
            for fn in filenames:
                fp = os.path.join(dirpath, fn)
                try:
                    size = os.path.getsize(fp)
                    os.remove(fp)
                    freed += size
                    removed += 1
                except OSError:
                    # in use / permission denied - skip it
                    errors += 1
        # try to drop now-empty subdirectories (best effort)
        for dirpath, dirnames, _files in os.walk(d, topdown=False):
            for sub in dirnames:
                try:
                    os.rmdir(os.path.join(dirpath, sub))
                except OSError:
                    pass
    return freed, removed, errors


def human_size(num):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(num) < 1024.0:
            return "{:.1f} {}".format(num, unit)
        num /= 1024.0
    return "{:.1f} PB".format(num)
