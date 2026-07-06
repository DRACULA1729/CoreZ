# CoreZ Advance Security

A desktop antivirus written in Python. CoreZ combines an MD5 signature blacklist,
YARA pattern rules and lightweight heuristics, with a quarantine vault, real-time
folder monitoring, junk cleanup and a RAM booster, all behind a Tkinter dashboard.

> Educational project. It is **not** a replacement for a production antivirus.

## Features

| Area | What it does |
|------|--------------|
| **Signature scanning** | MD5 hash lookup against a bundled database of ~85,000 known-malware hashes. |
| **YARA rules** | Pattern-based detection (`yara_rules/*.yar`) for families the hash list misses. |
| **Heuristics** | Flags double-extension tricks (`photo.jpg.exe`) and high-entropy (packed) executables. |
| **Quarantine vault** | Detected files are moved to a vault and XOR-neutralised, with restore / permanent-delete. Nothing is silently deleted. |
| **Real-time protection** | Watches chosen folders (via `watchdog`) and scans files as they appear/change. |
| **Junk cleaner** | Previews then clears OS/user temp and cache locations. |
| **RAM booster** | Closes idle installed apps to free memory (with a protected-process safelist). |
| **VirusTotal (optional)** | Looks a file up by SHA-256 (hash only — contents never uploaded). |

## Install

```bash
cd "CoreZ Project"
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The GUI uses Tkinter, which ships with Python on Windows/macOS but is a separate
package on many Linux distros:

```bash
# Debian / Ubuntu
sudo apt install python3-tk
```

## Run

```bash
python Loading.py     # splash screen -> main dashboard
# or launch the dashboard directly:
python gui.py
```

## Testing detection safely

Use the **EICAR test file** — a harmless standard string every antivirus is
expected to detect. Create it and run a Custom Scan on its folder:

```bash
printf 'X5O!P%%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' > eicar.com
```

CoreZ flags it via the `EICAR_Test_File` YARA rule. No real malware needed.

## Optional: VirusTotal

Set an API key via the environment (preferred) or in Settings:

```bash
export CoreZ_VT_API_KEY="your_key_here"
```

## Architecture

```
Loading.py        splash -> launches gui.py
gui.py            Tkinter dashboard; threaded scans, results table, all windows
engine.py         facade: RAM booster + backward-compatible scan wrappers
scanner.py        scan orchestration (signature + YARA + heuristic layers)
signatures.py     MD5/SHA-256 hashing + signature database
yara_scanner.py   compiles & matches yara_rules/*.yar
heuristics.py     entropy + double-extension checks
quarantine.py     vault: move / restore / delete + JSON manifest
realtime.py       watchdog-based real-time protection
junk.py           temp/cache cleaner
vt.py             optional VirusTotal hash lookup
config.py         persisted settings (corez_config.json)
Database/         Virushashe.txt (hashes) + virusinfo.txt (names)
```

Scans run on worker threads and report to the UI through a queue polled on the Tk
main loop, so the window never freezes.
