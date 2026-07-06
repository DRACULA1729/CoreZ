"""Optional VirusTotal hash lookups for CoreZ.

Uses the VirusTotal v3 API to look up a file by its SHA-256 - only the hash is
sent, never the file contents, so it is privacy-preserving. Requires an API key
(see config.vt_api_key). Fails soft: returns a status dict, never raises to the UI.
"""

import config
import signatures

try:
    import requests
    _REQUESTS_AVAILABLE = True
except ImportError:  # pragma: no cover
    requests = None
    _REQUESTS_AVAILABLE = False

_API = "https://www.virustotal.com/api/v3/files/{}"


def lookup_file(path, api_key=None):
    """Look up a file by SHA-256. Returns a dict with a 'status' key."""
    if not _REQUESTS_AVAILABLE:
        return {"status": "unavailable", "message": "requests not installed"}
    key = api_key or config.vt_api_key()
    if not key:
        return {"status": "no_key", "message": "No VirusTotal API key configured"}

    try:
        sha = signatures.file_sha256(path)
    except OSError as e:
        return {"status": "error", "message": str(e)}

    try:
        resp = requests.get(_API.format(sha), headers={"x-apikey": key}, timeout=20)
    except requests.RequestException as e:
        return {"status": "error", "message": str(e)}

    if resp.status_code == 404:
        return {"status": "unknown", "sha256": sha, "message": "Not seen by VirusTotal"}
    if resp.status_code == 401:
        return {"status": "error", "message": "Invalid VirusTotal API key"}
    if resp.status_code == 429:
        return {"status": "error", "message": "VirusTotal rate limit reached"}
    if resp.status_code != 200:
        return {"status": "error", "message": "HTTP {}".format(resp.status_code)}

    stats = resp.json().get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
    malicious = stats.get("malicious", 0)
    suspicious = stats.get("suspicious", 0)
    total = sum(stats.values()) if stats else 0
    return {
        "status": "ok",
        "sha256": sha,
        "malicious": malicious,
        "suspicious": suspicious,
        "total": total,
        "message": "{}/{} engines flagged this file".format(malicious + suspicious, total),
    }
