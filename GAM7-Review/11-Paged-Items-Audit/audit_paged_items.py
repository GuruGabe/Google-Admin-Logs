#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_paged_items.py
====================

PURPOSE
-------
GAM lists things with wrappers such as
        callGAPIpages(cd.users(), 'list', 'users', ...)
The third argument ('users') names the field of Google's answer that holds the
list.  If that name is wrong (typo, or Google renamed the field), GAM does NOT
crash: it quietly finds nothing and prints an empty result.  That is worse than
a crash because nobody notices.  This tool checks every such name against the
"response" description in Google's discovery documents.

HOW IT WORKS
------------
1. Reuse the helper functions of ../02-API-Method-Audit/audit_api_methods.py
   (loaded by file path) to work out which API each call belongs to.
2. For each callGAPIpages / yieldGAPIpages / callGAPIitems call whose method
   name and items name are plain strings, find the method in Google's
   document, follow its "response" -> schema reference, and read the list of
   property names of that response.
3. Report every call whose items name is not one of those properties.
Calls whose API cannot be pinned down with certainty are skipped (counted).

USAGE
-----
    python3 audit_paged_items.py <gam-src-folder> <discovery-cache-folder>

(The cache folder is the one made by ../01-Discovery-Fetch.)

SECURITY NOTES
--------------
Read only, no network access, no credentials, GAM code is parsed not executed.

Script written 11-21-2026.
"""
import ast                     # parse GAM's source into a tree
import importlib.util          # load the sibling tool by file path
import json                    # read discovery documents
import os                      # paths
import sys                     # arguments / exit code

PAGED = ("callGAPIpages", "yieldGAPIpages", "callGAPIitems")


def load_tool02():
    """Load ../02-API-Method-Audit/audit_api_methods.py as a module."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "02-API-Method-Audit", "audit_api_methods.py")
    spec = importlib.util.spec_from_file_location("audit_api_methods", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def find_method(doc, path, method):
    """Return the method dictionary at resource path 'a/b' in a document."""
    node = doc
    for part in [p for p in path.split("/") if p]:
        node = (node.get("resources") or {}).get(part)
        if node is None:
            return None
    return (node.get("methods") or {}).get(method)


def response_fields(doc, method_def):
    """Names of the fields in the method's response object."""
    ref = (method_def.get("response") or {}).get("$ref")
    schema = (doc.get("schemas") or {}).get(ref) or {}
    return set((schema.get("properties") or {}).keys())


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    gam_src, cache_dir = sys.argv[1], sys.argv[2]
    tool = load_tool02()

    with open(os.path.join(gam_src, "gam", "__init__.py"), encoding="utf-8") as handle:
        tree = ast.parse(handle.read())
    glapi = tool.load_glapi(gam_src)
    scopes = tool.collect_scope_maps(tree)     # variable -> (API, resource path)

    # Load every cached document: {(api, version): parsed json}
    docs = {}
    for name in os.listdir(cache_dir):
        if name.endswith(".json"):
            api, version = name[:-5].split("__", 1)
            with open(os.path.join(cache_dir, name), encoding="utf-8") as handle:
                docs[(api, version)] = json.load(handle)

    # GAM constant name ('DIRECTORY') -> (real api, version)
    const_to_key = {}
    for const in dir(glapi):
        value = getattr(glapi, const)
        if isinstance(value, str) and value in glapi._INFO:
            cfg = glapi._INFO[value]
            const_to_key[const] = (cfg.get("mappedAPI", value), cfg["version"])

    checked = skipped = 0
    problems = []
    for top in tree.body:
        if not isinstance(top, ast.FunctionDef):
            continue
        for node in ast.walk(top):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id in PAGED and len(node.args) >= 2):
                continue
            # The items name is the 3rd positional argument or items=...
            items = None
            if len(node.args) >= 3 and isinstance(node.args[2], ast.Constant):
                items = node.args[2].value
            for kw in node.keywords:
                if kw.arg == "items" and isinstance(kw.value, ast.Constant):
                    items = kw.value.value
            chain = tool.attr_chain(node.args[0])
            method_node = node.args[1]
            if not (items and chain and isinstance(method_node, ast.Constant)):
                skipped += 1
                continue
            # Which (API, resource path) could the service variable be?
            candidates = set()
            for table in (scopes.get(top.name, {}), scopes.get("<module>", {})):
                for const, base in table.get(chain[0], ()):
                    if const in const_to_key:
                        full = "/".join(list(base) + list(chain[1]))
                        candidates.add((const_to_key[const], full))
            fields, found = set(), False
            for key, full in candidates:
                doc = docs.get(key)
                if doc is None:
                    continue
                method_def = find_method(doc, full, method_node.value)
                if method_def:
                    found = True
                    fields |= response_fields(doc, method_def)
            if not found:
                skipped += 1          # could not tie to a known method
                continue
            checked += 1
            if items not in fields:
                problems.append((node.lineno, top.name, method_node.value,
                                 items, sorted(fields)))

    print("Paged calls checked : %d   (skipped, not certain: %d)" % (checked, skipped))
    print("Suspicious items names: %d" % len(problems))
    for line, scope, method, items, fields in problems:
        print("  line %-7d in %s: method %s, items=%r not in response fields %s"
              % (line, scope, method, items, fields[:10]))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
