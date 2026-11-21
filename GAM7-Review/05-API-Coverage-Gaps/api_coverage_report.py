#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
api_coverage_report.py
======================

PURPOSE
-------
Answers three questions about GAM7 and Google's APIs:

  1. COVERAGE  - For every API GAM already uses, which of Google's methods does
                 GAM never call?  (These are features Google offers that GAM
                 has no command for.)
  2. DEPRECATED - Does GAM call any method that Google has marked
                 "deprecated" in the API description?  (These will eventually
                 stop working.)
  3. CURRENCY  - Is GAM using the newest version of each API, and are there
                 Google Workspace / Cloud Identity APIs that GAM does not use
                 at all?

INPUTS (produced by the earlier tools in this review)
-----------------------------------------------------
  * the discovery cache folder written by ../01-Discovery-Fetch
  * method_audit.json written by ../02-API-Method-Audit
  * the list of ALL Google APIs (the "directory"), which this script downloads
    from the public URL https://www.googleapis.com/discovery/v1/apis
    (no credentials needed) unless you pass an already saved copy.

USAGE
-----
    python3 api_coverage_report.py <gam-src-folder> <discovery-cache> \
            <method_audit.json> <report-folder> [directory.json]

SECURITY NOTES
--------------
Read only.  The only network request is the anonymous download of Google's
public API directory, and only when you do not supply directory.json.

HONEST LIMITATIONS
------------------
* "Used by GAM" comes from the static scan.  Calls whose method name is held in
  a variable are only partly resolved, so the unused list can include a few
  methods that GAM does call dynamically.  Treat the lists as leads to verify,
  not as proof.
* "Not used" does NOT mean "should be added".  Many methods are irrelevant to
  administrators (for example Gmail 'users.watch' needs a Pub/Sub topic).
  The report only shows what exists.

Script written 11-21-2026.
"""

import importlib.util
import json
import os
import re
import sys
import urllib.request

# ---------------------------------------------------------------------------
# A hand written list of Google APIs that are relevant to a Google Workspace
# administrator but that GAM7 does NOT currently use.  It is the output of
# comparing Google's full directory (316 APIs on 11-21-2026) with GAM's
# glapi._INFO table and picking the ones an admin could plausibly want.
# Each entry:  api name -> why an administrator might care.
# This list is a judgement call, which is why it is written out in plain sight
# rather than computed.
# ---------------------------------------------------------------------------
WORKSPACE_RELEVANT = {
    "appsmarket":           "Workspace Marketplace API: inspect Marketplace apps / licenses installed in the domain",
    "cloudsearch":          "Cloud Search API: enterprise search data sources, identity sources, indexing",
    "script":               "Apps Script API: manage/deploy script projects, view execution metrics",
    "slides":               "Slides API: read/create/update presentations (GAM has Docs, Sheets and Forms but not Slides)",
    "workspaceevents":      "Workspace Events API: subscriptions to Drive/Chat/Meet events (push notifications)",
    "gmailpostmastertools": "Gmail Postmaster Tools: domain reputation, spam rate, SPF/DKIM/DMARC delivery stats",
    "dataportability":      "Data Portability API: export a user's Google data (offboarding / legal requests)",
    "chromewebstore":       "Chrome Web Store API: inspect/publish extension items",
    "verifiedaccess":       "Chrome Verified Access API: device attestation for Zero Trust",
    "androidmanagement":    "Android Management API: Android Enterprise devices and policies",
    "androiddeviceprovisioning": "Android Device Provisioning: zero-touch enrollment",
    "cloudasset":           "Cloud Asset Inventory: IAM/policy search across the organization",
    "logging":              "Cloud Logging: query audit logs exported to Cloud Logging",
    "securitycenter":       "Security Command Center: findings and posture",
    "mybusinessbusinessinformation": "Business Profile information (GAM only uses account management)",
    "marketingplatformadmin": "Google Marketing Platform admin: org/account links",
}


def load_glapi(gam_src):
    """Load gam/gamlib/glapi.py by path (it has no imports, so this is safe)."""
    path = os.path.join(gam_src, "gam", "gamlib", "glapi.py")
    spec = importlib.util.spec_from_file_location("glapi_standalone", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def all_methods(doc):
    """Return {'resource/path.method': method_dict} for a discovery document."""
    found = {}

    def walk(resources, prefix):
        for res_name, res in (resources or {}).items():
            path = prefix + [res_name]
            for method_name, method in (res.get("methods") or {}).items():
                found["%s.%s" % ("/".join(path), method_name)] = method
            walk(res.get("resources"), path)

    for method_name, method in (doc.get("methods") or {}).items():
        found[".%s" % method_name] = method
    walk(doc.get("resources"), [])
    return found


def version_key(version):
    """Sort key so that v1 < v1beta1 < v2 < v2beta ... roughly by number.

    Returns (major number, 1 if stable else 0, minor beta number).  Good
    enough to say "a newer stable version exists" for the APIs GAM uses.
    """
    match = re.search(r"v(\d+)(?:(alpha|beta)(\d*))?", version)
    if not match:
        return (0, 0, 0)
    major = int(match.group(1))
    stable = 0 if match.group(2) else 1
    return (major, stable, int(match.group(3) or 0))


def main():
    if len(sys.argv) not in (5, 6):
        print(__doc__)
        return 2
    gam_src, cache_dir, audit_json, report_dir = sys.argv[1:5]
    directory_file = sys.argv[5] if len(sys.argv) == 6 else None
    os.makedirs(report_dir, exist_ok=True)

    glapi = load_glapi(gam_src)
    with open(audit_json, encoding="utf-8") as handle:
        audit = json.load(handle)
    used_strict = {k: set(v) for k, v in audit["methods_used_by_gam"].items()}
    used_loose = {k: set(v) for k, v in audit.get("methods_used_loose_match", {}).items()}

    # ---- Google's public API directory (every API Google publishes) -------
    if directory_file:
        with open(directory_file, encoding="utf-8") as handle:
            directory = json.load(handle)
    else:
        url = "https://www.googleapis.com/discovery/v1/apis"
        with urllib.request.urlopen(url, timeout=60) as response:
            directory = json.loads(response.read().decode("utf-8"))
    # directory['items'] lists EVERY version of every API; keep a map of
    # api -> list of versions, and which one Google marks "preferred".
    versions_by_api = {}
    preferred = {}
    for item in directory["items"]:
        versions_by_api.setdefault(item["name"], []).append(item["version"])
        if item.get("preferred"):
            preferred[item["name"]] = item["version"]

    out = []                       # lines of the Markdown report
    out.append("# GAM7 API coverage, deprecation and currency report")
    out.append("")
    out.append("Generated 11-21-2026 by api_coverage_report.py (see script for method).")
    out.append("")

    # ---- 1. per-API coverage + 2. deprecated methods in use ---------------
    out.append("## 1. Coverage of the APIs GAM already uses")
    out.append("")
    out.append("`strict` = calls the static scan could tie to this API with certainty. "
               "`loose` = also matched by name only (variable passed through a helper).")
    out.append("")
    out.append("| API | version | Google methods | called (strict) | called (strict+loose) |")
    out.append("|---|---|---|---|---|")
    detail = []
    deprecated_in_use = []
    seen_docs = sorted(f for f in os.listdir(cache_dir) if f.endswith(".json"))
    for file_name in seen_docs:
        api, version = file_name[:-5].split("__", 1)
        with open(os.path.join(cache_dir, file_name), encoding="utf-8") as handle:
            doc = json.load(handle)
        methods = all_methods(doc)
        # Names in the audit are 'resource/path.method'; discovery uses the same.
        key = "%s %s" % (api, version)
        strict = {m.lstrip(".") for m in used_strict.get(key, set())}
        loose = strict | {m.lstrip(".") for m in used_loose.get(key, set())}
        normalized = {name.lstrip("."): meta for name, meta in methods.items()}
        total = len(normalized)
        n_strict = len(strict & set(normalized))
        n_loose = len(loose & set(normalized))
        out.append("| %s | %s | %d | %d | %d |" % (api, version, total, n_strict, n_loose))
        unused = sorted(set(normalized) - loose)
        detail.append((api, version, unused))
        # deprecated methods that GAM calls
        for name in sorted(loose & set(normalized)):
            meta = normalized[name]
            # Google flags deprecation either with a boolean 'deprecated' field
            # or by starting the method description with "Deprecated".  A
            # description that merely CONTAINS the word later on (for example
            # "Deprecated events cannot be imported") is NOT a deprecated
            # method, so we only look at the very start of the text.
            if meta.get("deprecated") or (meta.get("description") or "").lstrip().lower().startswith("deprecated"):
                certainty = "certain" if name in strict else "probable (name match only)"
                deprecated_in_use.append((api, version, name, certainty,
                                          (meta.get("description") or "")[:160].replace("\n", " ")))
        # deprecated parameters on methods GAM calls (informational only)
    out.append("")

    out.append("## 2. Methods GAM calls that Google marks deprecated")
    out.append("")
    if deprecated_in_use:
        for api, version, name, certainty, desc in deprecated_in_use:
            out.append("* **%s %s** `%s` [%s] - %s" % (api, version, name, certainty, desc))
    else:
        out.append("None found (checked the `deprecated` flag and descriptions "
                   "that start with the word Deprecated).")
    out.append("")

    # ---- 3. currency: newer versions available? ---------------------------
    out.append("## 3. API version currency")
    out.append("")
    out.append("| GAM name | GAM version | Google's preferred version | all versions Google lists | note |")
    out.append("|---|---|---|---|---|")
    for gam_name, cfg in sorted(glapi._INFO.items()):
        real = cfg.get("mappedAPI", gam_name)
        if cfg.get("localjson") or real not in versions_by_api:
            continue
        mine = cfg["version"]
        all_versions = sorted(set(versions_by_api[real]), key=version_key)
        pref = preferred.get(real, "?")
        note = ""
        if mine not in versions_by_api[real]:
            note = "VERSION NOT IN GOOGLE'S DIRECTORY"
        elif pref != "?" and version_key(pref) > version_key(mine):
            note = "newer preferred version exists"
        elif "beta" in mine or "alpha" in mine:
            note = "GAM uses a pre-release version"
        if note:
            out.append("| %s | %s | %s | %s | %s |" % (
                gam_name, mine, pref, ", ".join(all_versions), note))
    out.append("")

    # ---- 4. Workspace-relevant APIs GAM does not use ----------------------
    out.append("## 4. Workspace-relevant Google APIs GAM does not use at all")
    out.append("")
    gam_real_apis = {cfg.get("mappedAPI", name) for name, cfg in glapi._INFO.items()}
    out.append("| API | latest version | why an administrator might care |")
    out.append("|---|---|---|")
    for api, why in sorted(WORKSPACE_RELEVANT.items()):
        if api in gam_real_apis or api not in versions_by_api:
            continue
        out.append("| %s | %s | %s |" % (api, preferred.get(api, "?"), why))
    out.append("")

    # ---- 5. detail: unused methods ---------------------------------------
    out.append("## 5. Methods Google offers that GAM never calls (per API)")
    out.append("")
    for api, version, unused in detail:
        if not unused:
            continue
        out.append("### %s %s (%d not called)" % (api, version, len(unused)))
        out.append("")
        out.append(", ".join("`%s`" % m for m in unused))
        out.append("")

    text = "\n".join(out) + "\n"
    with open(os.path.join(report_dir, "api_coverage_report.md"), "w",
              encoding="utf-8") as handle:
        handle.write(text)
    print(text[:6000])
    print("... full report written to %s" % os.path.join(report_dir, "api_coverage_report.md"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
