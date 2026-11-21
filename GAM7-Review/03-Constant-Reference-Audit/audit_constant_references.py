#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_constant_references.py
============================

PURPOSE
-------
GAM's code is full of references such as
        Msg.INVALID_ENTITY          (a message text)
        Ent.USER                    (an "entity" type)
        GAPI.NOT_FOUND              (a Google error reason)
        GC.TIMEZONE                 (a configuration setting)
        Act.UPDATE                  (an "action" type)
If any one of those names is misspelled or was deleted, Python only finds out
when that exact line RUNS, and the user sees an AttributeError traceback.  With
84,000 lines of code, many lines run only for rare commands, so such mistakes
can hide for a long time.

This script checks ALL of them at once, without running any command:
for every   <Module>.<NAME>   reference in gam/__init__.py it asks the real,
imported object whether NAME exists.

HOW IT WORKS (plain English)
----------------------------
1. Import the gam package.  (Importing only defines functions and objects; it
   does not run any GAM command.)  This gives us the REAL objects:
   Msg, Ent, Act, GAPI, GC, GM, API, ...
2. Parse gam/__init__.py into an AST (Python's own parsed tree of the code).
3. Walk the tree.  Every time we see  Name.attribute  where Name is one of
   the objects above, call hasattr(object, attribute).
4. Print every reference that does not exist, with the line number.

IMPORTANT: this script must be run with a Python that has GAM's dependencies
installed (the same virtual environment you installed GAM into).  Example:

    python3 -m venv venv
    venv/bin/pip install /path/to/GAM          # installs GAM + dependencies
    venv/bin/python audit_constant_references.py /path/to/GAM/src

SECURITY NOTES
--------------
* Read only.  Importing gam creates the folder ~/.gam and a default gam.cfg
  the first time (GAM does this itself on any run).  No network access, no
  credentials are read or written.
* Nothing from the audited source is executed except the normal import-time
  definitions of the gam package.

Script written 11-21-2026.
"""

import ast        # Python's parser; lets us find every  X.y  reference
import json       # machine readable report
import os         # paths
import sys        # arguments, exit code

# The names GAM uses for its helper objects, as bound in gam/__init__.py.
# Each entry is the variable name used in the code we are scanning.
WATCHED = ["API", "GC", "GAPI", "GDATA", "GM", "Msg", "SKU", "UProp",
           "Act", "Cmd", "Ent", "Ind"]


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python audit_constant_references.py <gam-src-folder> [report-folder]")
        return 2
    gam_src = sys.argv[1]
    report_dir = sys.argv[2] if len(sys.argv) == 3 else None

    # Make 'import gam' find the source tree we were pointed at, even if an
    # older copy of GAM is installed in this Python environment.
    sys.path.insert(0, gam_src)
    import gam as gam_package            # runs gam/__init__.py definitions

    # Collect the real objects.  gam_package.Msg etc. exist because
    # gam/__init__.py does  "from gamlib import glmsgs as Msg"  at top level.
    objects = {}
    for name in WATCHED:
        if hasattr(gam_package, name):
            objects[name] = getattr(gam_package, name)
        else:
            print("NOTE: gam.%s is not defined at module level; skipping" % name)

    # Parse the main source file.
    main_file = os.path.join(gam_src, "gam", "__init__.py")
    with open(main_file, encoding="utf-8") as handle:
        tree = ast.parse(handle.read(), filename=main_file)

    checked = 0
    problems = []
    for node in ast.walk(tree):
        # We want the shape  Name.attribute , e.g.  Msg.NOT_FOUND
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) \
                and node.value.id in objects:
            checked += 1
            target = objects[node.value.id]
            if not hasattr(target, node.attr):
                problems.append({"line": node.lineno,
                                 "reference": "%s.%s" % (node.value.id, node.attr)})

    problems.sort(key=lambda row: row["line"])
    print("References checked : %d" % checked)
    print("Missing references : %d" % len(problems))
    for row in problems:
        print("  line %-7d %s" % (row["line"], row["reference"]))

    if report_dir:
        os.makedirs(report_dir, exist_ok=True)
        with open(os.path.join(report_dir, "constant_audit.json"), "w",
                  encoding="utf-8") as handle:
            json.dump({"checked": checked, "missing": problems}, handle, indent=1)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
