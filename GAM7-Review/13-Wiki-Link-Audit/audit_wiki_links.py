#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_wiki_links.py
===================

PURPOSE
-------
GAM ships its documentation as a folder of Markdown pages (the "wiki" folder).
Pages link to each other like  [Users - Gmail](Users-Gmail).  If a page is
renamed or removed, the link breaks and a reader lands on a "page not found".
This tool lists every link to a page that does not exist.

It also lists commands the wiki documents that GAM's own command tables do not
contain, but ONLY when you pass the GAM source folder as the second argument
(see "COMMAND CHECK" below).

HOW IT WORKS
------------
1. Find all  *.md  files in the wiki folder.  A page's name is its file name
   without ".md".  Names are compared WITHOUT regard to upper/lower case,
   because GitHub wiki page names are not case-sensitive.
2. Read each page line by line.  Lines inside ``` code fences are ignored so
   example text cannot create false alarms.
3. Find Markdown links  ](target)  .  Skip web links (http:, https:, mailto:).
   Remove any  #anchor  part and a trailing ".md".  If no page has that name,
   report it, with a close-match suggestion when there is one.
(Anchors - the #heading part - are NOT checked: GitHub's rules for turning a
heading into an anchor are intricate and a wrong guess would give false alarms.)

COMMAND CHECK (optional)
------------------------
When the GAM src folder is given, the tool imports GAM (so it must be run with
a Python that has GAM's libraries installed) and looks at every code-fenced
line that starts with  gam  , reads the first words after it (a verb and an
object, for example  "print users" ) and checks that GAM's command tables know
them.  This finds typos in the documentation such as "ensable csekeypair".
Expect some noise: GAM parses a few forms (like course-work, group-members)
with special code rather than tables, and GamUpdates.md is a history file that
mentions commands that no longer exist.  Read the list, do not trust it blindly.

USAGE
-----
    python3 audit_wiki_links.py <wiki-folder>
    <python-with-GAM> audit_wiki_links.py <wiki-folder> <gam-src-folder>

SECURITY NOTES
--------------
Read only.  No network.  The optional command check imports GAM, which creates
~/.gam on first use exactly as running GAM does.

Script written 11-21-2026.
"""
import collections      # defaultdict / Counter helpers
import difflib          # find "close" page names to suggest
import glob             # list files by pattern
import os               # paths
import re               # regular expressions to find links and tokens
import sys              # arguments / exit code


def page_names(wiki):
    """Return {lowercase name: real name} for every page in the folder."""
    return {os.path.basename(f)[:-3].lower(): os.path.basename(f)[:-3]
            for f in glob.glob(os.path.join(wiki, "*.md"))}


def iter_text_lines(path):
    """Yield (line number, line) for lines OUTSIDE code fences."""
    inside = False
    with open(path, encoding="utf-8", errors="replace") as handle:
        for number, line in enumerate(handle, 1):
            if line.startswith("```"):
                inside = not inside
                continue
            if not inside:
                yield number, line


def iter_code_lines(path):
    """Yield (line number, line) for lines INSIDE code fences."""
    inside = False
    with open(path, encoding="utf-8", errors="replace") as handle:
        for number, line in enumerate(handle, 1):
            if line.startswith("```"):
                inside = not inside
                continue
            if inside:
                yield number, line


def check_links(wiki):
    """Return {missing page: [(file, line), ...]} and the name table."""
    names = page_names(wiki)
    missing = collections.defaultdict(list)
    for path in sorted(glob.glob(os.path.join(wiki, "*.md"))):
        for number, line in iter_text_lines(path):
            # ](target)  or  ](target#anchor)  - target has no spaces or ')'
            for match in re.finditer(r"\]\(([^)\s#]+)(#[^)\s]*)?\)", line):
                target = match.group(1)
                if re.match(r"^(https?:|mailto:)", target):
                    continue                       # web links are not our job
                page = target[:-3] if target.endswith(".md") else target
                if page.lower() not in names:
                    missing[page].append((os.path.basename(path), number))
    return missing, names


def check_commands(wiki, gam_src):
    """Return {(kind, verb, object): [files]} for documented unknown commands."""
    sys.path.insert(0, gam_src)
    import gam                                   # GAM's real command tables
    main_tbl, main_alias = gam.MAIN_COMMANDS_WITH_OBJECTS, gam.MAIN_COMMANDS_OBJ_ALIASES
    user_tbl, user_alias = gam.USER_COMMANDS_WITH_OBJECTS, gam.USER_COMMANDS_OBJ_ALIASES
    verb_alias = {"create": "add", "add": "create", "del": "delete"}

    def known(table, aliases, verb, obj):
        for v in {verb, verb_alias.get(verb, verb)}:
            entry = table.get(v)
            if entry is None:
                continue
            objects = entry[1] if isinstance(entry, tuple) else entry
            for o in {obj, aliases.get(obj, obj)}:
                if o in objects:
                    return True
        return False

    def alternatives(token):
        """'print|show' or '(a|b)' -> ['print','show']; drop <placeholders>."""
        parts = re.split(r"[|()\[\]]", token.lower())
        return [p for p in parts if p and not p.startswith("<") and not p.startswith("*")]

    words_ok = set(gam.MAIN_COMMANDS) | set(gam.COMMANDS_MAP) | {
        "select", "redirect", "config", "csv", "loop", "batch", "tbatch",
        "multiprocess", "version", "help", "oauth", "oauth2", "calendar",
        "calendars", "resource", "resources", "course", "courses", "audit",
        "cros", "user", "users", "group", "groups", "report", "reports",
        "sendemail", "whatis", "list", "comment"}
    unknown = collections.defaultdict(set)
    for path in sorted(glob.glob(os.path.join(wiki, "*.md"))):
        for _number, line in iter_code_lines(path):
            if not line.startswith("gam "):
                continue
            tokens = line.split()
            if len(tokens) < 3:
                continue
            first = tokens[1]
            if first.startswith("<") and "user" in first.lower() \
                    and "typeentity" in first.lower():
                kind, verbs = "user", alternatives(tokens[2])
                objects = alternatives(tokens[3]) if len(tokens) > 3 else [""]
            elif first.startswith("<"):
                continue
            else:
                kind, verbs, objects = "main", alternatives(first), alternatives(tokens[2])
            for verb in verbs:
                if kind == "user":
                    verb = gam.USER_COMMANDS_ALIASES.get(verb, verb)
                for obj in objects:
                    if kind == "user":
                        if verb in gam.USER_COMMANDS or known(user_tbl, user_alias, verb, obj):
                            continue
                    else:
                        if verb in words_ok and verb not in main_tbl:
                            continue
                        if known(main_tbl, main_alias, verb, obj) or verb in gam.MAIN_COMMANDS:
                            continue
                    unknown[(kind, verb, obj)].add(os.path.basename(path))
    return unknown


def main():
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        return 2
    wiki = sys.argv[1]
    missing, names = check_links(wiki)
    print("Distinct missing pages: %d" % len(missing))
    for page, where in sorted(missing.items()):
        close = difflib.get_close_matches(page.lower(), list(names), 1, 0.75)
        hint = "  (maybe %s)" % names[close[0]] if close else ""
        print("  %-28s from %s%s" % (page, where[:3], hint))
    if len(sys.argv) == 3:
        unknown = check_commands(wiki, sys.argv[2])
        print()
        print("Documented commands not in GAM's tables: %d (expect some noise)" % len(unknown))
        for (kind, verb, obj), files in sorted(unknown.items()):
            print("  %s: %s %s   %s" % (kind, verb, obj, sorted(files)[:2]))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
