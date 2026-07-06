"""Signature database and file hashing for CoreZ.

The on-disk database is the abuse.ch-style pair shipped with the project:
    Database/Virushashe.txt  - one 32-char MD5 digest per line
    Database/virusinfo.txt   - one malware-family name per line

The two files are not 1:1 (info has more lines than hashes), so we pair them
positionally and drop the unreachable tail. Everything is loaded once into an
in-memory dict for O(1) lookups, and hashing is done in chunks so we never read
a whole (possibly huge) file into memory.
"""

import hashlib
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(SCRIPT_DIR, "Database")

_HASH_FILE = os.path.join(DB_DIR, "Virushashe.txt")
_INFO_FILE = os.path.join(DB_DIR, "virusinfo.txt")

# Read files in 1 MiB blocks when hashing.
_CHUNK = 1024 * 1024


def file_md5(path):
    """Return the lowercase hex MD5 of a file, read in chunks."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(_CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def file_sha256(path):
    """Return the lowercase hex SHA-256 of a file, read in chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(_CHUNK), b""):
            h.update(block)
    return h.hexdigest()


class SignatureDB:
    """Lazy-loaded MD5 -> malware-name lookup table."""

    def __init__(self, hash_file=_HASH_FILE, info_file=_INFO_FILE):
        self._hash_file = hash_file
        self._info_file = info_file
        self._db = None  # dict[str, str]

    def _load(self):
        hashes = []
        with open(self._hash_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip().lower()  # strip whitespace/CR and normalise case
                if line:
                    hashes.append(line)

        names = []
        with open(self._info_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                names.append(line.strip())

        # Pair positionally; names past the last hash are unreachable.
        db = {}
        for h, name in zip(hashes, names):
            db[h] = name or "Unknown.Malware"
        # Any hashes without a paired name still count as malicious.
        for h in hashes[len(names):]:
            db.setdefault(h, "Unknown.Malware")
        self._db = db

    @property
    def db(self):
        if self._db is None:
            self._load()
        return self._db

    def __len__(self):
        return len(self.db)

    def match(self, path):
        """Return the malware name if the file's MD5 is known-bad, else None."""
        return self.db.get(file_md5(path))

    def match_hash(self, md5_hex):
        """Look up an already-computed lowercase MD5 hex digest."""
        return self.db.get(md5_hex.lower())


# Module-level default instance shared across scanner / real-time / GUI.
default_db = SignatureDB()
