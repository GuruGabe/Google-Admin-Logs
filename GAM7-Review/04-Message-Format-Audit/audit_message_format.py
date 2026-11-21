#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_message_format.py
=======================

PURPOSE
-------
GAM keeps its user-visible text in gam/gamlib/glmsgs.py as templates, for
example:
        NOT_FOUND = '{0} {1} not found'
and the program fills them in like this:
        Msg.NOT_FOUND.format('User', 'bob@example.com')
If the number or names of the arguments do not match the placeholders in the
template, Python raises IndexError ("Replacement index 1 out of range") or
KeyError at the moment the message would be printed.  That is an especially
nasty failure: it usually happens inside an ERROR handler, so the user loses
the real error message and sees a Python crash instead.

This script checks every   Msg.<NAME>.format(...)   call in gam/__init__.py.

WHAT IT CHECKS
--------------
For each call it reads the real template text from the imported Msg module and
compares:
  * Numbered placeholders  {0} {1}  /  empty placeholders  {} {}
      -> the call must supply at least that many positional arguments.
  * Named placeholders  {name}
      -> the call must supply  name=...  for each one.
  * Extra arguments that the template never uses are reported as WARNINGS
    (harmless to Python, but usually a sign of a mistake).
Calls that use *args or **kwargs cannot be counted, so they are skipped and
counted separately.

USAGE
-----
Run with the Python that has GAM's dependencies installed:

    venv/bin/python audit_message_format.py /path/to/GAM/src [report-folder]

SECURITY NOTES
--------------
Read only; no network; no credentials.  Importing gam creates ~/.gam on first
use exactly like running any GAM command does.

Script written 11-21-2026.
"""

import ast          # parse the source into a tree
import json         # machine readable report
import os           # paths
import string       # string.Formatter().parse() splits a template into fields
import sys          # arguments / exit code


def template_fields(template):
    """Split a format template into (auto_count, explicit_indexes, names).

    Example:  '{0} of {1} for {name}'  ->  (0, {0, 1}, {'name'})
              '{} and {}'              ->  (2, set(), set())
    """
    auto = 0                   # how many bare {} placeholders
    explicit = set()           # numbers used like {0}
    names = set()              # names used like {user}
    for _literal, field, _spec, _conv in string.Formatter().parse(template):
        if field is None:
            continue           # plain text segment, no placeholder
        # A field can look like  0.attr  or  name[key]  - keep the first part.
        head = field.split(".")[0].split("[")[0]
        if head == "":
            auto += 1
        elif head.isdigit():
            explicit.add(int(head))
        else:
            names.add(head)
    return auto, explicit, names


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python audit_message_format.py <gam-src-folder> [report-folder]")
        return 2
    gam_src = sys.argv[1]
    report_dir = sys.argv[2] if len(sys.argv) == 3 else None

    sys.path.insert(0, gam_src)            # make 'import gam' use this source
    import gam as gam_package
    msg_module = gam_package.Msg            # gamlib/glmsgs.py

    main_file = os.path.join(gam_src, "gam", "__init__.py")
    with open(main_file, encoding="utf-8") as handle:
        tree = ast.parse(handle.read(), filename=main_file)

    errors = []        # certain crashes
    warnings = []      # unused arguments
    skipped = 0        # calls we could not count (*args / **kwargs)
    checked = 0

    for node in ast.walk(tree):
        # Looking for:  Msg.NAME.format( ... )
        if not (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "format"
                and isinstance(node.func.value, ast.Attribute)
                and isinstance(node.func.value.value, ast.Name)
                and node.func.value.value.id == "Msg"):
            continue
        msg_name = node.func.value.attr
        template = getattr(msg_module, msg_name, None)
        if not isinstance(template, str):
            # Not a plain string (e.g. a function); nothing to compare.
            continue
        # *args or **kwargs make the real count unknowable at parse time.
        if any(isinstance(a, ast.Starred) for a in node.args) \
                or any(k.arg is None for k in node.keywords):
            skipped += 1
            continue
        checked += 1
        auto, explicit, names = template_fields(template)
        needed_positional = max([auto] + [i + 1 for i in explicit]) \
            if (auto or explicit) else 0
        given_positional = len(node.args)
        given_names = {k.arg for k in node.keywords}
        problem = []
        if given_positional < needed_positional:
            problem.append("needs %d positional args, got %d"
                           % (needed_positional, given_positional))
        missing_names = names - given_names
        if missing_names:
            problem.append("missing named args: %s" % ", ".join(sorted(missing_names)))
        row = {"line": node.lineno, "message": msg_name,
               "template": template[:80]}
        if problem:
            row["problem"] = "; ".join(problem)
            errors.append(row)
            continue
        extra = []
        if given_positional > needed_positional:
            extra.append("%d unused positional args"
                         % (given_positional - needed_positional))
        unused_names = given_names - names
        if unused_names:
            extra.append("unused named args: %s" % ", ".join(sorted(unused_names)))
        if extra:
            row["problem"] = "; ".join(extra)
            warnings.append(row)

    print("Msg.X.format() calls checked : %d (skipped %d with *args/**kwargs)"
          % (checked, skipped))
    print("Certain crashes (too few args): %d" % len(errors))
    for row in errors:
        print("  line %-7d Msg.%-40s %s\n               template: %r"
              % (row["line"], row["message"], row["problem"], row["template"]))
    print("Warnings (unused args)         : %d" % len(warnings))
    for row in warnings:
        print("  line %-7d Msg.%-40s %s" % (row["line"], row["message"], row["problem"]))

    if report_dir:
        os.makedirs(report_dir, exist_ok=True)
        with open(os.path.join(report_dir, "message_format_audit.json"), "w",
                  encoding="utf-8") as handle:
            json.dump({"checked": checked, "skipped": skipped,
                       "errors": errors, "warnings": warnings}, handle, indent=1)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
