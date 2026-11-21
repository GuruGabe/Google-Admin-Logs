#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_fields_masks.py
=====================

PURPOSE
-------
Most GAM calls pass a "fields" string that tells Google which parts of the
answer to send back, for example
        fields='nextPageToken,users(primaryEmail,name(fullName))'
If a name inside that string does not exist in Google's description of the
answer (typo, renamed field, or wrong syntax), the call either fails with a
400 error or - worse - the missing data just never arrives, and GAM prints
blank columns or "Unknown" without any error message.

This tool checks every literal fields string GAM passes to callGAPI,
callGAPIpages, callGAPIitems and yieldGAPIpages against the response schema in
Google's discovery documents.

FIELDS SYNTAX (the small language we check)
-------------------------------------------
    a,b            two top level fields
    a/b            field b inside field a
    a(b,c)         fields b and c inside a   (works for lists of objects too)
    *              wildcard: everything at that level (not checked)
A dot (a.b) is NOT part of this syntax.

HOW IT WORKS
------------
1. Reuse tool 02 (loaded by file path) to work out which API a call belongs to.
2. Find the method in Google's document and follow  response -> $ref  to the
   schema that describes the answer.
3. Parse the fields string into a tree, then walk the schema level by level
   (following $ref links and the 'items' of arrays).  A name that is not a
   property at its level is "unknown".
4. If a call could belong to several APIs, it is only reported when the name is
   unknown in ALL of them (benefit of the doubt).
Strings built at run time (f-strings, variables) cannot be checked and are
skipped; the count of skipped strings is printed.

USAGE
-----
    python3 audit_fields_masks.py <gam-src-folder> <discovery-cache-folder>

SECURITY NOTES
--------------
Read only, no network access, no credentials, GAM code is parsed not executed.

Script written 11-21-2026.
"""
import ast                     # parse GAM's source into a tree
import importlib.util          # load tool 02 by path
import json                    # read discovery documents
import os                      # paths
import sys                     # arguments / exit code


def load_tool02():
    """Load ../02-API-Method-Audit/audit_api_methods.py as a module."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "02-API-Method-Audit", "audit_api_methods.py")
    spec = importlib.util.spec_from_file_location("audit_api_methods", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def find_method(doc, path, method):
    """Return the method dictionary at resource path 'a/b' (or None)."""
    node = doc
    for part in [p for p in path.split("/") if p]:
        node = (node.get("resources") or {}).get(part)
        if node is None:
            return None
    return (node.get("methods") or {}).get(method)


def follow(doc, schema):
    """Follow $ref links until we reach a schema with real content."""
    hops = 0
    while schema and "$ref" in schema and hops < 20:    # 20 = loop guard
        schema = doc["schemas"].get(schema["$ref"])
        hops += 1
    return schema or {}


def element_schema(doc, schema):
    """For an array schema return the schema of its elements, else itself."""
    schema = follow(doc, schema)
    if schema.get("type") == "array":
        return element_schema(doc, schema.get("items"))
    return schema


def parse_fields(text):
    """Parse 'a,b(c,d/e),f' into [(name, [children] or None), ...]."""
    position = 0

    def parse_list():
        nonlocal position
        result = []
        while position < len(text):
            name = ""
            while position < len(text) and text[position] not in ",()":
                name += text[position]
                position += 1
            children = None
            if position < len(text) and text[position] == "(":
                position += 1                     # skip '('
                children = parse_list()
                if position < len(text) and text[position] == ")":
                    position += 1                 # skip ')'
            result.append((name.strip(), children))
            if position < len(text) and text[position] == ",":
                position += 1
                continue
            break
        return result

    return parse_list()


def check_level(doc, schema, items, trail, unknown):
    """Check every (name, children) pair against the schema at this level."""
    node = element_schema(doc, schema)
    properties = node.get("properties")
    if properties is None:
        return          # free-form object (additionalProperties): cannot judge
    for name, children in items:
        current = node
        reached = True
        parts = [p for p in name.split("/") if p]
        for index, part in enumerate(parts):
            if part == "*":
                current = None                    # wildcard - stop checking
                break
            current = element_schema(doc, current)
            level = current.get("properties")
            if level is None:
                current = None
                break
            if part not in level:
                unknown.append(trail + "/".join(parts[: index + 1]))
                reached = False
                break
            current = level[part]
        if reached and children and current is not None:
            check_level(doc, current, children, trail + name + ".", unknown)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    gam_src, cache_dir = sys.argv[1], sys.argv[2]
    tool = load_tool02()
    with open(os.path.join(gam_src, "gam", "__init__.py"), encoding="utf-8") as handle:
        tree = ast.parse(handle.read())
    glapi = tool.load_glapi(gam_src)
    scopes = tool.collect_scope_maps(tree)

    docs = {}
    for name in os.listdir(cache_dir):
        if name.endswith(".json"):
            api, version = name[:-5].split("__", 1)
            with open(os.path.join(cache_dir, name), encoding="utf-8") as handle:
                docs[(api, version)] = json.load(handle)
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
                    and node.func.id in tool.WRAPPERS and len(node.args) >= 2):
                continue
            fields_nodes = [k.value for k in node.keywords if k.arg == "fields"]
            if not fields_nodes or not (isinstance(fields_nodes[0], ast.Constant)
                                        and isinstance(fields_nodes[0].value, str)
                                        and fields_nodes[0].value):
                skipped += 1
                continue
            fields_text = fields_nodes[0].value
            chain = tool.attr_chain(node.args[0])
            method_node = node.args[1]
            if not (chain and isinstance(method_node, ast.Constant)):
                skipped += 1
                continue
            candidates = set()
            for table in (scopes.get(top.name, {}), scopes.get("<module>", {})):
                for const, base in table.get(chain[0], ()):
                    if const in const_to_key:
                        candidates.add((const_to_key[const],
                                        "/".join(list(base) + list(chain[1]))))
            outcomes = []
            for key, full in candidates:
                doc = docs.get(key)
                if doc is None:
                    continue
                method_def = find_method(doc, full, method_node.value)
                if not method_def or not method_def.get("response"):
                    continue
                unknown = []
                check_level(doc, {"$ref": method_def["response"]["$ref"]},
                            parse_fields(fields_text), "", unknown)
                outcomes.append((key, unknown))
            if not outcomes:
                skipped += 1
                continue
            checked += 1
            if all(unknown for _key, unknown in outcomes):
                problems.append((node.lineno, top.name, method_node.value,
                                 fields_text, outcomes[0][1][:4]))

    print("fields strings checked: %d   (skipped, not checkable: %d)" % (checked, skipped))
    print("with unknown field names: %d" % len(problems))
    for line, scope, method, text, unknown in problems:
        print("  line %-7d in %s (%s): fields=%r -> unknown %s"
              % (line, scope, method, text[:70], unknown))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
