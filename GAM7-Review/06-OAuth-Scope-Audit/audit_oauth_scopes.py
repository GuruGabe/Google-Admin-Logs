#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_oauth_scopes.py
=====================

PURPOSE
-------
Every Google API call needs an OAuth "scope" - a permission string such as
    https://www.googleapis.com/auth/admin.directory.user
GAM keeps lists of the scopes it asks for in gam/gamlib/glapi.py
(_CLIENT_SCOPES, _SVCACCT_SCOPES, ...).  When GAM builds an API client it
compares the user's granted scopes with the scopes that API's description lists
(see buildGAPIObject in gam/__init__.py).  If a scope in GAM's list does not
exist in Google's description any more (Google renamed or retired it):
    * the scope may be silently ignored, so the user never gets the permission
      and every command for that API then fails with a permission error, or
    * GAM stops with "no scopes for API".

This script checks every scope string GAM lists against Google's current
descriptions, and also lists scopes Google offers that GAM never asks for.

HOW IT WORKS
------------
1. Load glapi.py by path (it has no imports) and read its scope tables.
2. For each table entry, find the Google API it belongs to and read the list of
   scopes from that API's discovery document ("auth" -> "oauth2" -> "scopes").
3. A scope is "known" if it is in that list, OR in glapi.EXTRA_SCOPES (scopes
   GAM documents as valid although Google's description omits them), OR the
   entry is on a short list of known exceptions below.
4. If an entry says  'subscopes': ['readonly']  then scope + '.readonly' is
   checked as well.

USAGE
-----
    python3 audit_oauth_scopes.py <gam-src-folder> <discovery-cache> [report-folder]

SECURITY NOTES
--------------
Read only, no network, no credentials.

Script written 11-21-2026.
"""

import importlib.util   # load glapi.py by file path
import json             # read discovery documents / write report
import os               # paths
import sys              # arguments / exit code

# Scope tables inside glapi.py that hold dictionaries with an 'api' and a
# 'scope' key.  Names are exactly as they appear in the source file.
SCOPE_TABLES = ["_CLIENT_SCOPES", "_COMMANDDATA_CLIENT_SCOPES",
                "_TODRIVE_CLIENT_SCOPES", "_SVCACCT_SCOPES",
                "_SVCACCT_SPECIAL_SCOPES", "_USER_SVCACCT_ONLY_SCOPES"]

# Scopes that every Google account has and that no API description lists.
ALWAYS_VALID = {
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
}


# Scopes that ARE valid but that Google's discovery documents do not list.
# Each is reported by this audit as "unknown" if not excluded here, so the
# reason for every exception is written down.  If Google later adds them to
# the documents, the exception becomes harmless.
KNOWN_DOC_GAPS = {
    # The My Business Account Management discovery document has an empty
    # "auth" section, but business.manage is the documented scope.
    "https://www.googleapis.com/auth/business.manage":
        "scope missing from Google's discovery document (documented scope)",
    # GAM ships datastudio-v1.json itself and that file lists no scopes.
    "https://www.googleapis.com/auth/datastudio":
        "GAM's bundled datastudio-v1.json has no scope list",
    "https://www.googleapis.com/auth/datastudio.readonly":
        "GAM's bundled datastudio-v1.json has no scope list",
    # Drive Activity v2 only reads activity for files the caller can see, so
    # GAM intentionally pairs it with a Drive scope (see the entry's name:
    # 'must pair with Drive API').  drive.readonly belongs to the Drive API.
    "https://www.googleapis.com/auth/drive.readonly":
        "intentional pairing with the Drive API",
}


def load_module(path, name):
    """Load a Python file by path and return it as a module object."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def discovery_scopes(doc):
    """Return the set of scope URLs in a discovery document ('' if none)."""
    return set(((doc.get("auth") or {}).get("oauth2") or {}).get("scopes", {}))


def main():
    if len(sys.argv) not in (3, 4):
        print(__doc__)
        return 2
    gam_src, cache_dir = sys.argv[1], sys.argv[2]
    report_dir = sys.argv[3] if len(sys.argv) == 4 else None

    glapi = load_module(os.path.join(gam_src, "gam", "gamlib", "glapi.py"),
                        "glapi_standalone")

    # Load every cached discovery document: {(api, version): scope set}
    scopes_by_doc = {}
    for name in sorted(os.listdir(cache_dir)):
        if name.endswith(".json"):
            api, version = name[:-5].split("__", 1)
            with open(os.path.join(cache_dir, name), encoding="utf-8") as handle:
                scopes_by_doc[(api, version)] = discovery_scopes(json.load(handle))
    # Also GAM's bundled local documents (datastudio, ...).
    gam_dir = os.path.join(gam_src, "gam")
    for name in sorted(os.listdir(gam_dir)):
        if name.endswith(".json") and "-" in name:
            api, version = name[:-5].rsplit("-", 1)
            with open(os.path.join(gam_dir, name), encoding="utf-8") as handle:
                scopes_by_doc.setdefault((api, version),
                                         discovery_scopes(json.load(handle)))

    # glapi constant VALUE ('directory') -> (real api, version)
    def doc_key(api_value):
        cfg = glapi._INFO[api_value]
        return (cfg.get("mappedAPI", api_value), cfg["version"])

    problems = []        # scopes GAM asks for that Google no longer lists
    checked = 0
    requested = set()    # every scope string GAM asks for (for the reverse check)
    for table_name in SCOPE_TABLES:
        for entry in getattr(glapi, table_name):
            api_value = entry["api"]
            # Most entries hold ONE scope string.  A few (Drive Activity,
            # Forms, Meet) hold a LIST of scopes that must be granted
            # together, so normalise both shapes into a list.
            scope_field = entry["scope"]
            scope_list = scope_field if isinstance(scope_field, list) else [scope_field]
            wanted = []
            for scope in scope_list:
                if not scope:
                    continue             # e.g. the Chrome Version History API
                wanted.append(scope)
                if "readonly" in entry.get("subscopes", []):
                    wanted.append(scope + ".readonly")
            for one in wanted:
                requested.add(one)
                checked += 1
                if one in ALWAYS_VALID or one in KNOWN_DOC_GAPS:
                    continue
                known = scopes_by_doc.get(doc_key(api_value))
                if known is None:
                    # No document to compare against (e.g. legacy API).
                    continue
                extra = set(glapi.EXTRA_SCOPES.get(api_value, []))
                if one not in known and one not in extra:
                    problems.append({"table": table_name, "api": api_value,
                                     "entry": entry["name"], "scope": one})

    print("Scope strings checked : %d" % checked)
    print("Not in Google's list  : %d" % len(problems))
    for row in problems:
        print("  [%s] %s (%s)\n      %s" % (row["table"], row["entry"],
                                           row["api"], row["scope"]))

    # ---- reverse direction: scopes Google offers for APIs GAM uses, that
    # GAM never requests anywhere.  Informational only.
    offered_unrequested = {}
    for _name, cfg in glapi._INFO.items():
        key = (cfg.get("mappedAPI", _name), cfg["version"])
        for scope in scopes_by_doc.get(key, set()):
            if scope not in requested and scope not in ALWAYS_VALID:
                offered_unrequested.setdefault("%s %s" % key, set()).add(scope)
    print()
    print("Scopes Google lists for GAM's APIs that GAM never requests (informational):")
    for key in sorted(offered_unrequested):
        print("  %s" % key)
        for scope in sorted(offered_unrequested[key]):
            print("      %s" % scope)

    if report_dir:
        os.makedirs(report_dir, exist_ok=True)
        with open(os.path.join(report_dir, "scope_audit.json"), "w",
                  encoding="utf-8") as handle:
            json.dump({"checked": checked, "unknown_scopes": problems,
                       "offered_not_requested": {
                           k: sorted(v) for k, v in offered_unrequested.items()}},
                      handle, indent=1)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
