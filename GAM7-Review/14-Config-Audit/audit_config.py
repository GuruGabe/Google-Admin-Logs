#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_config.py
===============

PURPOSE
-------
GAM reads its settings from gam.cfg.  The list of settings, their types, their
limits and their default values live in gam/gamlib/glcfg.py, and the wiki page
gam.cfg.md documents them.  Three things can go wrong, and this tool checks all
three:

  1. The two tables inside glcfg.py disagree.  "Defaults" holds the default
     value of every setting and "VAR_INFO" holds its type/limits.  A setting in
     one table but not the other breaks GAM when the configuration is loaded.
  2. A default value breaks the setting's own rules (for example an integer
     default of 5 for a setting whose allowed range is 10-20).
  3. The documentation (gam.cfg.md) is out of date: it lists a setting that
     no longer exists, forgets one that does, or states a default value or
     range that differs from the code.

HOW IT WORKS
------------
* glcfg.py has no imports except os, so it is loaded straight from its path.
* For check 2 each default is tested by type: booleans must be true/false,
  integers/floats inside VAR_LIMITS, choices inside VAR_CHOICES (GAM compares
  choices in lower case), single characters of length 1 after the quotes GAM
  writes around them are removed.
  A short list of KNOWN_SENTINELS covers settings whose default is a deliberate
  "not set yet" marker that GAM replaces while starting up (see the comments in
  that list).
* For check 3 the wiki's "Variables" section is split into one block per
  setting and the "Default:" and "Range:" lines are compared with the code.
  Defaults written as prose ("Blank", "0, do not ...") are compared by their
  first word only when they are numbers; prose is otherwise ignored.

USAGE
-----
    python3 audit_config.py <gam-src-folder> <wiki-folder>

SECURITY NOTES
--------------
Read only, no network, nothing from GAM is executed except loading glcfg.py.

Script written 11-21-2026.
"""
import importlib.util   # load glcfg.py by file path
import os               # paths
import re               # parse the wiki text
import sys              # arguments / exit code

# Settings whose default does not follow the normal rules on purpose.  GAM
# turns each into a real value during start-up (gam/__init__.py around the
# "TODRIVE_NOBROWSER" lines of the config loader).
KNOWN_SENTINELS = {
    "todrive_nobrowser": "empty means 'derive from no_browser'",
    "todrive_noemail": "empty means 'derive from no_browser'",
    "todrive_sheet_timestamp": "'copy' means 'copy todrive_timestamp'",
    "todrive_sheet_timeformat": "'copy' means 'copy todrive_timeformat'",
    # 'section' is not a normal setting: it is the name of the active gam.cfg
    # section, so it has no fixed default.
    "section": "name of the active section",
}

# Settings that exist in the tables on purpose but are not described in the
# wiki's Variables list.  no_update_check is kept only so old gam.cfg files
# still load; GAM ignores it (see GamUpdate.txt: "Eliminated automatic checking
# for a new GAM version, no_update_check in gam.cfg is now ignored").
KNOWN_UNDOCUMENTED = {"no_update_check"}


def load_glcfg(gam_src):
    """Load gam/gamlib/glcfg.py as a standalone module."""
    path = os.path.join(gam_src, "gam", "gamlib", "glcfg.py")
    spec = importlib.util.spec_from_file_location("glcfg_standalone", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def unquote(text):
    """GAM writes some defaults with quotes around them, e.g. '"' - drop them."""
    text = str(text)
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "'\"":
        return text[1:-1]
    return text


def check_defaults(g):
    """Checks 1 and 2.  Returns a list of problem strings."""
    problems = []
    defaults, info = g.Defaults, g.VAR_INFO
    for name in sorted(set(defaults) - set(info)):
        problems.append("%s is in Defaults but not in VAR_INFO" % name)
    for name in sorted(set(info) - set(defaults)):
        problems.append("%s is in VAR_INFO but not in Defaults" % name)
    for name, meta in info.items():
        if name not in defaults or name in KNOWN_SENTINELS:
            continue
        value, kind = defaults[name], meta[g.VAR_TYPE]
        limits, choices = meta.get(g.VAR_LIMITS), meta.get(g.VAR_CHOICES)
        try:
            if kind == g.TYPE_BOOLEAN:
                if value not in (g.TRUE, g.FALSE):
                    problems.append("%s: boolean default %r" % (name, value))
            elif kind in (g.TYPE_INTEGER, g.TYPE_FLOAT):
                number = int(value) if kind == g.TYPE_INTEGER else float(value)
                if limits and ((limits[0] is not None and number < limits[0])
                               or (limits[1] is not None and number > limits[1])):
                    problems.append("%s: default %s outside limits %s" % (name, value, limits))
            elif kind == g.TYPE_CHOICE:
                if str(value).lower() not in {str(c).lower() for c in choices}:
                    problems.append("%s: default %r not a choice" % (name, value))
            elif kind == g.TYPE_CHARACTER:
                if len(unquote(value)) != 1:
                    problems.append("%s: character default %r" % (name, value))
        except (ValueError, TypeError) as err:
            problems.append("%s: default %r unusable (%s)" % (name, value, err))
    return problems


def check_wiki(g, wiki_file):
    """Check 3.  Returns a list of problem strings."""
    problems = []
    with open(wiki_file, encoding="utf-8") as handle:
        text = handle.read()
    # The "Variables" section lists each setting as a name line followed by
    # indented description lines.  Split it into one block per setting.
    section = text.split("## Variables")[1].split("## Set configuration")[0]
    blocks = re.split(r"\n(?=[a-z][a-z0-9_]{3,}\n\s)", section)
    documented = set()
    for block in blocks:
        name = block.split("\n", 1)[0].strip()
        if name not in g.Defaults:
            if re.match(r"^[a-z][a-z0-9_]{3,}$", name):
                problems.append("wiki documents %s, which is not in the code" % name)
            continue
        documented.add(name)
        match = re.search(r"^\s*Default:\s*(.*)$", block, flags=re.M)
        if match:
            doc_default = unquote(match.group(1).strip())
            code_default = unquote(g.Defaults[name])
            # Only compare when the documented default is a plain number or a
            # single word; prose such as 'Blank, address from ...' is skipped.
            if re.fullmatch(r"-?\d+(\.\d+)?|[A-Za-z0-9_.]+", doc_default) \
                    and name not in KNOWN_SENTINELS \
                    and doc_default.lower() != code_default.lower() \
                    and not (doc_default.lower() == "blank" and code_default == ""):
                problems.append("%s: wiki default %r, code default %r"
                                % (name, doc_default, code_default))
            elif doc_default == "" and code_default != "" and name not in KNOWN_SENTINELS:
                problems.append("%s: wiki default is empty, code default %r"
                                % (name, code_default))
        limits = g.VAR_INFO[name].get(g.VAR_LIMITS)
        match = re.search(r"^\s*Range:\s*(-?\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?|Unlimited)",
                          block, flags=re.M)
        if match and limits:
            low = float(match.group(1))
            high = None if match.group(2) == "Unlimited" else float(match.group(2))
            code_low = 0 if limits[0] is None else float(limits[0])
            code_high = None if limits[1] is None else float(limits[1])
            if low != code_low or high != code_high:
                problems.append("%s: wiki range %s, code limits %s"
                                % (name, match.group(0).strip(), limits))
    for name in sorted(set(g.Defaults) - documented - KNOWN_UNDOCUMENTED):
        problems.append("%s exists in the code but has no block in the wiki list" % name)
    return problems


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    g = load_glcfg(sys.argv[1])
    wiki_file = os.path.join(sys.argv[2], "gam.cfg.md")
    code_problems = check_defaults(g)
    wiki_problems = check_wiki(g, wiki_file)
    print("settings in code: %d" % len(g.Defaults))
    print("Code table problems: %d" % len(code_problems))
    for item in code_problems:
        print("  " + item)
    print("Wiki versus code differences: %d" % len(wiki_problems))
    for item in wiki_problems:
        print("  " + item)
    return 1 if (code_problems or wiki_problems) else 0


if __name__ == "__main__":
    sys.exit(main())
