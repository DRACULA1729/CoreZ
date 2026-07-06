"""CoreZ engine facade.

Historically this module held the scanner, signature DB and RAM booster all in
one file. Scanning/detection now lives in dedicated modules (signatures,
scanner, yara_scanner, heuristics, quarantine); this file keeps the RAM booster
and provides thin backward-compatible wrappers so older entry points keep working.

Importing this module has NO side effects (the old version scanned a hardcoded
path at import time, which crashed the app).
"""

import os
import sys

import psutil

import scanner as _scanner
import quarantine as _quarantine

if sys.platform == "win32":
    import winreg
else:
    winreg = None


# --------------------------------------------------------------------------
# Scanning wrappers (delegate to the scanner module)
# --------------------------------------------------------------------------
# Kept for backward compatibility. New code should use scanner.Scanner directly.
virusName = []
virusPath = []


def quickScan(path):
    """Scan a path; populate the legacy virusName/virusPath lists with threats."""
    result = _scanner.default_scanner.scan(path)
    virusName.clear()
    virusPath.clear()
    for d in result.threats:
        virusName.append("{}::File:: {}".format(d.name, d.path))
        virusPath.append(d.path)
    return result


# virusScanner was a byte-for-byte duplicate of quickScan; keep the name as an alias.
virusScanner = quickScan


def virusRemover(path):
    """Scan a path and quarantine (not delete) every actionable threat."""
    result = quickScan(path)
    if not result.threats:
        return 0
    for d in result.threats:
        try:
            _quarantine.default_quarantine.quarantine(d.path, d.name, d.severity)
        except OSError:
            continue
    return len(result.threats)


# --------------------------------------------------------------------------
# RAM booster (Windows-oriented, with a portable psutil fallback)
# --------------------------------------------------------------------------
def get_installed_software_executables():
    software_executables = []
    if winreg is None:
        return software_executables

    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
    ]
    for path in registry_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            try:
                                display_icon = winreg.QueryValueEx(subkey, "DisplayIcon")[0]
                                executable_ = os.path.basename(display_icon)
                                executable_name = executable_.split(".exe")[0] + ".exe"
                                if display_name and executable_name:
                                    software_executables.append((display_name, executable_name))
                            except FileNotFoundError:
                                continue
                    except EnvironmentError:
                        continue
        except EnvironmentError:
            continue
    return software_executables


# Processes we must never kill - killing these would take down the desktop/OS.
_PROTECTED_PROCESSES = {
    "explorer.exe", "winlogon.exe", "csrss.exe", "services.exe", "lsass.exe",
    "svchost.exe", "system", "systemd", "init", "gnome-shell", "python", "python3",
    "corez", "wininit.exe", "dwm.exe",
}


def _kill_process_by_name(proc_name):
    if proc_name.lower() in _PROTECTED_PROCESSES:
        return
    for proc in psutil.process_iter(attrs=["name"]):
        name = (proc.info.get("name") or "").lower()
        if name == proc_name.lower() and name not in _PROTECTED_PROCESSES:
            try:
                proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue


def ramboost():
    """Free RAM by closing idle installed apps. Returns a human-readable summary."""
    running = {(p.info.get("name") or "").lower()
               for p in psutil.process_iter(attrs=["name"])}
    installed = {exe.lower() for _name, exe in get_installed_software_executables()}
    targets = [name for name in installed
               if name in running and name not in _PROTECTED_PROCESSES]

    before = psutil.virtual_memory().available
    for name in targets:
        try:
            _kill_process_by_name(name)
        except Exception:
            continue
    after = psutil.virtual_memory().available
    freed_mb = max(0, (after - before)) / (1024 * 1024)

    if not installed:
        return "RAM Booster is only available on Windows."
    return "RAM Boosted - closed {} app(s), freed ~{:.0f} MB.".format(len(targets), freed_mb)
