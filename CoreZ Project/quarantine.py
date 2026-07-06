"""Quarantine vault for CoreZ.

Instead of deleting a detected file outright, we move it into a vault and
XOR-obfuscate its bytes. This makes the file non-executable / harmless at rest,
keeps it out of the way of further scans, and lets the user restore a false
positive. A JSON manifest records everything needed to restore or purge.
"""

import json
import os
import time
import uuid

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_DIR = os.path.join(SCRIPT_DIR, "quarantine_vault")
MANIFEST = os.path.join(VAULT_DIR, "manifest.json")

# Single-byte XOR key. Not cryptographic - just enough to defang the payload
# so it can't execute or be re-matched while it sits in the vault.
_XOR_KEY = 0x2A


def _xor_bytes(data):
    return bytes(b ^ _XOR_KEY for b in data)


class Quarantine:
    def __init__(self, vault_dir=VAULT_DIR):
        self.vault_dir = vault_dir
        self.manifest_path = os.path.join(vault_dir, "manifest.json")

    def _ensure_vault(self):
        os.makedirs(self.vault_dir, exist_ok=True)

    def _load_manifest(self):
        try:
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_manifest(self, entries):
        self._ensure_vault()
        tmp = self.manifest_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2)
        os.replace(tmp, self.manifest_path)

    def list_entries(self):
        return self._load_manifest()

    def quarantine(self, path, detection_name="", severity=""):
        """Move ``path`` into the vault (obfuscated). Returns the entry id."""
        self._ensure_vault()
        entry_id = uuid.uuid4().hex
        stored_name = entry_id + ".corezq"
        stored_path = os.path.join(self.vault_dir, stored_name)

        with open(path, "rb") as src:
            data = src.read()
        with open(stored_path, "wb") as dst:
            dst.write(_xor_bytes(data))

        entry = {
            "id": entry_id,
            "original_path": os.path.abspath(path),
            "stored_name": stored_name,
            "detection": detection_name,
            "severity": severity,
            "size": len(data),
            "quarantined_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        }
        entries = self._load_manifest()
        entries.append(entry)
        self._save_manifest(entries)

        # Only remove the original after the vault copy is safely written.
        os.remove(path)
        return entry_id

    def _find(self, entry_id, entries):
        for e in entries:
            if e["id"] == entry_id:
                return e
        return None

    def restore(self, entry_id, dest=None):
        """De-obfuscate and move a quarantined file back. Returns restored path."""
        entries = self._load_manifest()
        entry = self._find(entry_id, entries)
        if entry is None:
            raise KeyError(entry_id)

        stored_path = os.path.join(self.vault_dir, entry["stored_name"])
        target = dest or entry["original_path"]
        os.makedirs(os.path.dirname(target) or ".", exist_ok=True)

        with open(stored_path, "rb") as src:
            data = _xor_bytes(src.read())
        with open(target, "wb") as dst:
            dst.write(data)

        os.remove(stored_path)
        entries = [e for e in entries if e["id"] != entry_id]
        self._save_manifest(entries)
        return target

    def delete(self, entry_id):
        """Permanently purge a quarantined file from the vault."""
        entries = self._load_manifest()
        entry = self._find(entry_id, entries)
        if entry is None:
            raise KeyError(entry_id)
        stored_path = os.path.join(self.vault_dir, entry["stored_name"])
        try:
            os.remove(stored_path)
        except FileNotFoundError:
            pass
        entries = [e for e in entries if e["id"] != entry_id]
        self._save_manifest(entries)


default_quarantine = Quarantine()
