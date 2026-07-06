"""YARA rule loading and matching for CoreZ.

Compiles every ``*.yar`` file under ``yara_rules/`` once and matches files
against them. If yara-python is not installed, the scanner degrades gracefully
to a no-op so the rest of the app keeps working.
"""

import os

try:
    import yara
    _YARA_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    yara = None
    _YARA_AVAILABLE = False

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_DIR = os.path.join(SCRIPT_DIR, "yara_rules")

# Don't feed enormous files to YARA; hashing/heuristics still cover them.
_MAX_YARA_BYTES = 32 * 1024 * 1024


class YaraScanner:
    """Compiles the rule directory lazily and matches files against it."""

    def __init__(self, rules_dir=RULES_DIR):
        self._rules_dir = rules_dir
        self._rules = None
        self._compiled = False

    @property
    def available(self):
        return _YARA_AVAILABLE

    def _compile(self):
        self._compiled = True
        if not _YARA_AVAILABLE or not os.path.isdir(self._rules_dir):
            self._rules = None
            return
        filepaths = {}
        for entry in sorted(os.listdir(self._rules_dir)):
            if entry.endswith((".yar", ".yara")):
                filepaths[entry] = os.path.join(self._rules_dir, entry)
        if not filepaths:
            self._rules = None
            return
        # A single bad rule file shouldn't kill the whole engine.
        try:
            self._rules = yara.compile(filepaths=filepaths)
        except yara.Error:
            self._rules = None

    @property
    def rules(self):
        if not self._compiled:
            self._compile()
        return self._rules

    def match(self, path):
        """Return a list of (rule_name, description, severity) for a file."""
        rules = self.rules
        if rules is None:
            return []
        try:
            if os.path.getsize(path) > _MAX_YARA_BYTES:
                return []
            matches = rules.match(path, timeout=30)
        except (yara.Error, OSError):
            return []
        results = []
        for m in matches:
            meta = getattr(m, "meta", {}) or {}
            results.append((
                m.rule,
                meta.get("description", m.rule),
                meta.get("severity", "suspicious"),
            ))
        return results


default_scanner = YaraScanner()
