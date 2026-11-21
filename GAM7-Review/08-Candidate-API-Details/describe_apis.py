#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
describe_apis.py
================

PURPOSE
-------
Prints a plain-language outline of one or more Google APIs: every resource,
every method (with its HTTP verb and URL path), the required parameters and the
OAuth scopes.  It is meant for planning NEW GAM commands: before anybody writes
code for an API GAM does not use yet (for example Apps Script or the Workspace
Marketplace), this shows exactly what Google offers and which permissions an
administrator would have to grant.

HOW IT WORKS
------------
1. For each API name you give, ask Google's public API directory for the newest
   "preferred" version and the URL of its discovery document.
2. Download that document (public, no login needed).
3. Walk through its resources and methods and write a Markdown outline.

USAGE
-----
    python3 describe_apis.py <output-file.md> <api> [<api> ...]

    Example:
    python3 describe_apis.py candidates.md appsmarket script slides

SECURITY NOTES
--------------
* Only downloads public documents; no credentials or personal data are sent.
* TLS certificate verification stays ON (the Python default).
* API names are validated against a strict pattern before being used, so a
  typo or hostile argument cannot be turned into a different URL.

Script written 11-21-2026.
"""

import json              # parse Google's JSON documents
import re                # validate the API names we are given
import sys               # command line arguments
import urllib.request    # download the public documents

DIRECTORY_URL = "https://www.googleapis.com/discovery/v1/apis"
# An API name is letters/digits only (Google names look like 'appsmarket').
SAFE_API_NAME = re.compile(r"^[A-Za-z0-9]+$")


def fetch_json(url):
    """Download a URL and return the parsed JSON.  Raises on any failure."""
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def outline(doc, out):
    """Append a Markdown outline of one discovery document to the list 'out'."""
    out.append("## %s %s - %s" % (doc.get("name"), doc.get("version"), doc.get("title")))
    out.append("")
    out.append((doc.get("description") or "").strip())
    out.append("")
    out.append("Base URL: `%s%s`" % (doc.get("rootUrl", ""), doc.get("servicePath", "")))
    scopes = ((doc.get("auth") or {}).get("oauth2") or {}).get("scopes", {})
    out.append("")
    out.append("OAuth scopes:")
    for scope, info in sorted(scopes.items()):
        out.append("* `%s` - %s" % (scope, info.get("description", "")))
    if not scopes:
        out.append("* (none listed)")
    out.append("")
    out.append("| resource | method | HTTP | path | required parameters |")
    out.append("|---|---|---|---|---|")

    def add_methods(path, methods):
        for name, method in sorted((methods or {}).items()):
            required = sorted(p for p, meta in (method.get("parameters") or {}).items()
                              if meta.get("required"))
            out.append("| %s | %s | %s | `%s` | %s |" % (
                path or "(service)", name, method.get("httpMethod", ""),
                method.get("path", ""), ", ".join(required)))

    def walk(resources, prefix):
        for res_name, res in sorted((resources or {}).items()):
            path = "/".join(prefix + [res_name])
            add_methods(path, res.get("methods"))
            walk(res.get("resources"), prefix + [res_name])

    add_methods("", doc.get("methods"))
    walk(doc.get("resources"), [])
    out.append("")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    output_file = sys.argv[1]
    names = sys.argv[2:]
    for name in names:
        if not SAFE_API_NAME.match(name):
            print("Refusing unsafe API name: %r" % name)
            return 2

    directory = fetch_json(DIRECTORY_URL)
    # Build {api name: discovery document URL of the preferred version}.
    preferred = {item["name"]: item["discoveryRestUrl"]
                 for item in directory["items"] if item.get("preferred")}
    out = ["# Candidate Google APIs - outline", "",
           "Generated 11-21-2026 by describe_apis.py from Google's public "
           "discovery documents.", ""]
    for name in names:
        if name not in preferred:
            out.append("## %s - NOT FOUND in Google's API directory" % name)
            out.append("")
            continue
        outline(fetch_json(preferred[name]), out)
    with open(output_file, "w", encoding="utf-8") as handle:
        handle.write("\n".join(out) + "\n")
    print("Wrote %s (%d APIs requested)" % (output_file, len(names)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
