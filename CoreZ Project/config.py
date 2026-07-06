"""Persistent local settings for CoreZ (stored next to the app as JSON).

The VirusTotal API key is read from the CoreZ_VT_API_KEY environment variable
first (so secrets need not live on disk), falling back to the config file.
"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "corez_config.json")

_DEFAULTS = {
    "realtime_paths": [os.path.expanduser("~")],
    "use_yara": True,
    "use_heuristics": True,
    "auto_quarantine_realtime": True,
    "vt_api_key": "",
}


def load():
    data = dict(_DEFAULTS)
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data.update(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return data


def save(data):
    tmp = CONFIG_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, CONFIG_PATH)


def vt_api_key(cfg=None):
    env = os.environ.get("CoreZ_VT_API_KEY")
    if env:
        return env
    if cfg is None:
        cfg = load()
    return cfg.get("vt_api_key", "")
