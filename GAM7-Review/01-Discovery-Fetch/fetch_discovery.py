#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_discovery.py
==================

PURPOSE
-------
Downloads Google's current "Discovery Documents" (a machine readable
description of every method of every Google API) for every API that GAM7 is
configured to use.  The downloaded files are saved to a cache folder so the
other audit scripts (02-API-Method-Audit, 03-API-Coverage-Gaps) can read them
without needing network access again.

WHY THIS MATTERS
----------------
GAM7 builds its API clients at RUN TIME from Google's discovery documents
(see getService() in gam/__init__.py).  If Google renames or removes a method,
GAM will crash only when that exact command is run.  By comparing GAM's source
code to the discovery documents ahead of time we can find those problems
before a user hits them.

HOW GAM7 FINDS ITS DISCOVERY DOCUMENTS (we copy the same logic)
--------------------------------------------------------------
gam/gamlib/glapi.py has a dictionary called _INFO.  Each entry has:
    version      - the API version, for example 'v1' or 'directory_v1'
    v2discovery  - True  -> use https://<api>.googleapis.com/$discovery/rest?version=<ver>
                   False -> use https://www.googleapis.com/discovery/v1/apis/<api>/<ver>/rest
    mappedAPI    - (optional) the real Google API name when GAM uses a nicer
                   internal name (e.g. GAM's 'directory' is Google's 'admin')
    localjson    - (optional) True when GAM ships its own JSON file instead of
                   downloading one (these are skipped here - they are not on
                   Google's servers)

USAGE
-----
    python3 fetch_discovery.py <path-to-gam-src-folder> <cache-folder>

    Example:
    python3 fetch_discovery.py /home/user/gam-team/gam/src ./discovery_cache

SECURITY NOTES
--------------
* Only reads public, unauthenticated Google URLs.  No credentials, tokens or
  personal data are ever sent.
* Uses only the Python standard library (no third-party code is installed).
* TLS certificate checking is left ON (the Python default).  Never disable it.
* Output file names are built from a fixed allow-list pattern so a malicious
  value in glapi.py cannot write outside the cache folder.

Script written 11-21-2026.
"""

# ---------------------------------------------------------------------------
# Imports.  All of these ship with Python itself.
# ---------------------------------------------------------------------------
import json                 # read/write JSON files
import os                   # file and folder handling
import re                   # regular expressions, used to validate file names
import sys                  # command line arguments and exit codes
import urllib.request       # downloads web pages
import urllib.error         # the errors urllib can raise
import time                 # used to pause briefly between retries

# URL templates that mirror what GAM7 itself uses.
# {api} and {ver} are replaced with the real values for each API.
V2_URL = "https://{api}.googleapis.com/$discovery/rest?version={ver}"
V1_URL = "https://www.googleapis.com/discovery/v1/apis/{api}/{ver}/rest"

# Two APIs GAM uses are OLD "GData" APIs (domain shared Contacts, and Email
# Audit).  They were never described by a discovery document, so Google always
# answers 404 for them.  That is normal, so they are reported as "skipped"
# instead of as a problem.  (Whether Google still serves those APIs at all
# cannot be learned from this tool - see FINDINGS-11-21-2026.md section 3.)
LEGACY_NO_DISCOVERY = {"contacts", "email-audit"}

# A file name is only accepted if it is letters, digits, dash, underscore, dot.
# This blocks values like "../../etc/passwd" from being used as a file name.
SAFE_NAME = re.compile(r"^[A-Za-z0-9._-]+$")


def load_gam_api_table(gam_src):
    """Import GAM's glapi module and return its _INFO dictionary.

    gam_src is the folder that CONTAINS the 'gam' package (i.e. .../GAM/src).

    We deliberately do NOT write 'import gam.gamlib.glapi'.  Importing any
    part of the 'gam' package first runs gam/__init__.py, which is an
    84,000 line file that needs many third party libraries and starts
    reading GAM's configuration.  glapi.py, however, has NO imports of its
    own - it is just constants - so we load that single file directly from
    its path.  This is faster, needs no extra libraries, and cannot touch
    credentials.
    """
    import importlib.util                      # lets us load a file by path
    glapi_path = os.path.join(gam_src, "gam", "gamlib", "glapi.py")
    spec = importlib.util.spec_from_file_location("glapi_standalone", glapi_path)
    glapi = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(glapi)             # runs the constants file
    return glapi._INFO


def download(url, tries=3):
    """Download one URL and return the parsed JSON, or None on failure.

    We retry a few times because the network (or the proxy) can briefly fail.
    """
    last_error = None
    for attempt in range(1, tries + 1):
        try:
            # timeout=60 means "give up if the server is silent for 60 sec".
            with urllib.request.urlopen(url, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            # 404 means Google no longer serves that API/version.  That is a
            # FINDING, not a transient problem, so do not retry.
            if err.code == 404:
                return {"__error__": "HTTP 404 (API or version not found)"}
            last_error = "HTTP %s" % err.code
        except (urllib.error.URLError, TimeoutError, ValueError) as err:
            last_error = str(err)
        time.sleep(2 * attempt)   # wait 2s, 4s, 6s between attempts
    return {"__error__": last_error}


def main():
    # ---- 1. Read command line arguments --------------------------------
    if len(sys.argv) != 3:
        print("Usage: python3 fetch_discovery.py <gam-src-folder> <cache-folder>")
        return 2
    gam_src, cache = sys.argv[1], sys.argv[2]
    os.makedirs(cache, exist_ok=True)

    # ---- 2. Load GAM's own API table ----------------------------------
    info = load_gam_api_table(gam_src)

    # Many GAM entries map to the same real Google API+version (for example
    # all of the CHAT_* entries use Google's 'chat' API).  Collect the unique
    # (real api, version, v2discovery) combinations so each is fetched once.
    wanted = {}
    for gam_name, cfg in info.items():
        if cfg.get("localjson"):
            continue                       # GAM ships its own file; skip
        real_api = cfg.get("mappedAPI", gam_name)
        key = (real_api, cfg["version"], bool(cfg["v2discovery"]))
        wanted.setdefault(key, []).append(gam_name)

    # ---- 3. Download each document -----------------------------------
    problems = []
    skipped = 0            # legacy APIs that are expected to have no document
    for (api, ver, v2), gam_names in sorted(wanted.items()):
        file_name = "%s__%s.json" % (api, ver)
        if not SAFE_NAME.match(file_name):
            problems.append((api, ver, "unsafe file name, skipped"))
            continue
        out_path = os.path.join(cache, file_name)
        url = (V2_URL if v2 else V1_URL).format(api=api, ver=ver)
        doc = download(url)
        if api in LEGACY_NO_DISCOVERY and doc and "404" in doc.get("__error__", ""):
            print("skipped %-28s %-14s legacy GData API, no discovery document (expected)"
                  % (api, ver))
            skipped += 1
            continue
        if doc is None or "__error__" in doc:
            reason = (doc or {}).get("__error__", "unknown")
            problems.append((api, ver, reason))
            print("FAILED  %-28s %-14s %s" % (api, ver, reason))
            continue
        with open(out_path, "w", encoding="utf-8") as handle:
            json.dump(doc, handle)
        print("ok      %-28s %-14s used by GAM as: %s" %
              (api, ver, ", ".join(sorted(gam_names))))

    # ---- 4. Summary --------------------------------------------------
    print()
    print("Downloaded %d of %d discovery documents into %s (%d legacy APIs skipped as expected)" %
          (len(wanted) - len(problems) - skipped, len(wanted), cache, skipped))
    if problems:
        print("PROBLEMS (these APIs may be broken or retired):")
        for api, ver, reason in problems:
            print("   %s %s -> %s" % (api, ver, reason))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
