#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_api_methods.py
====================

PURPOSE
-------
Statically (WITHOUT running GAM and WITHOUT any credentials) checks that every
Google API method GAM7 calls still exists in Google's current API description.

If GAM calls  callGAPI(cd.orgunits(), 'getFoo', ...)  but Google's directory API
has no 'getFoo' method on the 'orgunits' resource, then the user gets a Python
AttributeError (a crash) the moment that command runs.  This script finds those
before any user does.

HOW IT WORKS (plain English)
----------------------------
1. Read GAM's big source file (gam/__init__.py) and turn it into an AST.
   An AST ("abstract syntax tree") is Python's own parsed representation of
   the code, so we can ask questions like "show me every function call named
   callGAPI" without fragile text searching.
2. Find every place a variable is created from one of GAM's API builder
   functions, e.g.:
        cd = buildGAPIObject(API.DIRECTORY)
        user, gmail, jcount = buildGAPIServiceObject(API.GMAIL, user, i, count)
   and remember "variable cd is the DIRECTORY API".
3. Find every API call in two shapes:
        callGAPI(cd.orgunits(), 'list', ...)      <- GAM's wrapper
        cd.orgunits().list(...)                   <- a direct call
   (callGAPIpages and callGAPIitems are wrappers of the first shape.)
4. Look up (API, resource path, method) in the downloaded discovery documents
   (see ../01-Discovery-Fetch/fetch_discovery.py).
5. Report anything that does not exist.

HONEST LIMITATIONS
------------------
* If a service object is handed to a helper function as a parameter, the script
  cannot always tell which API it is.  Those calls are checked in "loose mode":
  the method only has to exist in AT LEAST ONE API.  They are listed in the
  "unresolved but found somewhere" count, so you know how much was verified
  strictly versus loosely.
* It checks that method NAMES exist (and that the resource path is right).  It
  does NOT check the keyword arguments passed to the method; see
  ../03-API-Param-Audit for that.
* Methods that exist only in Google's DEVELOPER PREVIEW (not in the public
  document) will be reported as missing even though GAM may handle them with a
  special developer-preview API key.  Those are tagged separately.

USAGE
-----
    python3 audit_api_methods.py <gam-src-folder> <discovery-cache-folder> <report-folder>

    Example:
    python3 audit_api_methods.py /home/user/gam-team/gam/src \
        /tmp/discovery_cache ./reports

SECURITY NOTES
--------------
* Read-only: never executes GAM code.  The source is only parsed (ast.parse),
  never imported or run.
* No network access, no credentials.
* Output files are written only inside the report folder you name.

Script written 11-21-2026.
"""

import ast            # Python's built in parser; turns source text into a tree
import importlib.util  # lets us load glapi.py by file path (see below)
import json           # read discovery files, write the machine readable report
import os             # paths and folders
import re             # regular expressions (parameter name clean-up)
import sys            # command line arguments / exit code
from collections import defaultdict   # dict that auto-creates missing entries

# ---------------------------------------------------------------------------
# GAM functions that BUILD a service object.  The first argument (or the
# keyword 'api') is an API constant such as API.DIRECTORY.
# The value is the default API used when the call passes no argument at all.
# ---------------------------------------------------------------------------
BUILDERS = {
    "buildGAPIObject": None,
    "buildGAPIServiceObject": None,
    "buildGAPIObjectNoAuthentication": None,
    "buildChatServiceObject": "CHAT",      # signature: (api=API.CHAT, ...)
    "buildMeetServiceObject": None,
    "getAPIService": None,
    "getService": None,
}

# GAM functions that WRAP an API call: (service_chain, 'methodName', ...).
WRAPPERS = {"callGAPI", "callGAPIpages", "callGAPIitems", "yieldGAPIpages"}

# Keyword arguments that belong to GAM's wrapper functions themselves and are
# consumed by the wrapper, NOT forwarded to Google.  Everything else a caller
# passes by keyword is forwarded to the Google API method and must be a real
# parameter of that method.  (Taken from the def lines of callGAPI,
# callGAPIpages, yieldGAPIpages and callGAPIitems in gam/__init__.py.)
WRAPPER_OWN_KWARGS = {
    "bailOnInternalError", "bailOnTransientError", "bailOnInvalidError",
    "softErrors", "mapNotFound", "throwReasons", "retryReasons", "triesLimit",
    "pageMessage", "messageAttribute", "maxItems", "noFinalize",
    "pageArgsInBody",
}

# How many POSITIONAL arguments each wrapper really takes.  callGAPI is
# (service, function); the paging wrappers are (service, function, items).
# Anything extra silently lands in the NEXT parameter - for callGAPI that is
# bailOnInternalError - which changes retry behavior without any error.
MAX_POSITIONAL = {"callGAPI": 2, "callGAPIpages": 3,
                  "yieldGAPIpages": 3, "callGAPIitems": 3}

# Methods that exist on every googleapiclient Resource object and therefore are
# never in a discovery document.  Calling them is always fine.
CLIENT_BUILTINS = {
    "execute", "next_chunk", "close", "new_batch_http_request", "batch",
    "add", "from_json", "to_json", "_next",
}


def load_glapi(gam_src):
    """Load gam/gamlib/glapi.py as a standalone module (it has no imports).

    Returns the loaded module so we can read its constants (API.DIRECTORY ->
    'directory') and its _INFO table (which real Google API/version each uses).
    """
    path = os.path.join(gam_src, "gam", "gamlib", "glapi.py")
    spec = importlib.util.spec_from_file_location("glapi_standalone", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Module level store of allowed keyword arguments for every API method:
#   PARAMS[((api, version), 'resource/path', 'method')] = {allowed names}
# It is filled by index_document() while the discovery documents are loaded.
PARAMS = {}

# Same keys, but only the parameters Google marks "required": true.  A call
# that leaves one out makes googleapiclient raise
#     TypeError: Missing required parameter "xyz"
REQUIRED = {}


def python_param_name(name):
    """Convert a discovery parameter name to the Python keyword googleapiclient
    exposes.  The library replaces every character that is not a letter, digit
    or underscore with '_' (so 'resource.name' becomes 'resource_name') and
    prefixes a leading digit with '_'.  We mirror that so comparisons match.
    """
    fixed = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    if fixed and fixed[0].isdigit():
        fixed = "_" + fixed
    return fixed


def index_document(key, doc):
    """Parse one discovery document.

    key  - (api name, version)
    doc  - the parsed JSON of the discovery document

    Returns {resource path: {method names}}.  As a side effect fills PARAMS
    with the keyword arguments each method accepts, following exactly the
    rules googleapiclient uses when it builds the Python client:
      * every entry in the method's 'parameters'
      * 'body'                      when the method has a 'request' section
      * 'media_body' and 'media_mime_type'  when it supports media upload
      * every API-wide parameter in the document's top level 'parameters'
        (these are things like fields, alt, key, prettyPrint, ...)
    """
    methods_by_path = defaultdict(set)
    global_params = {python_param_name(n) for n in (doc.get("parameters") or {})}

    def add_methods(path_key, methods):
        for method_name, method in (methods or {}).items():
            methods_by_path[path_key].add(method_name)
            allowed = set(global_params)
            allowed |= {python_param_name(n)
                        for n in (method.get("parameters") or {})}
            if method.get("request"):
                allowed.add("body")
            if method.get("supportsMediaUpload"):
                allowed |= {"media_body", "media_mime_type"}
            PARAMS[(key, path_key, method_name)] = allowed
            REQUIRED[(key, path_key, method_name)] = {
                python_param_name(n)
                for n, meta in (method.get("parameters") or {}).items()
                if meta.get("required")}

    def walk(resources, prefix):
        """Recursively record every resource and the methods under it."""
        for res_name, res in (resources or {}).items():
            path = prefix + [res_name]
            path_key = "/".join(path)
            methods_by_path.setdefault(path_key, set())
            add_methods(path_key, res.get("methods"))
            walk(res.get("resources"), path)

    add_methods("", doc.get("methods"))
    walk(doc.get("resources"), [])
    return methods_by_path


def load_discovery_index(cache_dir):
    """Read every downloaded discovery document and index its methods.

    Returns {(real_api, version): {resource path: {method names}}}.
    The empty path '' means "methods directly on the service root".
    """
    index = {}
    for name in sorted(os.listdir(cache_dir)):
        if not name.endswith(".json"):
            continue
        # Files are saved as <api>__<version>.json by fetch_discovery.py
        api, version = name[:-5].split("__", 1)
        with open(os.path.join(cache_dir, name), encoding="utf-8") as handle:
            doc = json.load(handle)
        index[(api, version)] = index_document((api, version), doc)
    return index


def load_local_json_docs(gam_src, index):
    """Add the discovery files that GAM ships INSIDE its own package.

    glapi._INFO marks a few APIs with 'localjson': True (Data Studio, Contact
    Delegation, Service Account Lookup).  GAM carries its own copy of their
    description, named like  datastudio-v1.json  in the gam/ folder.  They are
    indexed exactly like the downloaded ones.  Key = (api name, version).
    """
    gam_dir = os.path.join(gam_src, "gam")
    for name in sorted(os.listdir(gam_dir)):
        if not name.endswith(".json") or "-" not in name:
            continue
        api, version = name[:-5].rsplit("-", 1)
        if (api, version) in index:
            continue
        with open(os.path.join(gam_dir, name), encoding="utf-8") as handle:
            doc = json.load(handle)
        index[(api, version)] = index_document((api, version), doc)


def attr_chain(node):
    """Turn  cd.orgunits()  or  iam.projects().serviceAccounts()  into
    ('cd', ['orgunits'])  /  ('iam', ['projects', 'serviceAccounts']).

    Returns (variable_name, [resource names]) or None if the expression is
    not a simple "variable followed by resource() calls" shape.
    """
    resources = []
    while True:
        # A call with no arguments, like  .orgunits()
        if isinstance(node, ast.Call) and not node.args and not node.keywords \
                and isinstance(node.func, ast.Attribute):
            resources.append(node.func.attr)
            node = node.func.value
        elif isinstance(node, ast.Name):
            resources.reverse()          # we collected them right-to-left
            return node.id, resources
        else:
            return None


def api_constant_from_arg(call, default_name):
    """Given a builder call node, return the API constant NAME it uses.

    For  buildGAPIObject(API.DIRECTORY)  this returns 'DIRECTORY'.
    Returns None when the argument is not a plain  API.<NAME>  expression
    (for example a variable), in which case we cannot resolve it statically.
    """
    arg = None
    if call.args:
        arg = call.args[0]
    else:
        for kw in call.keywords:
            if kw.arg == "api":
                arg = kw.value
    if arg is None:
        return default_name
    if isinstance(arg, ast.Attribute) and isinstance(arg.value, ast.Name) \
            and arg.value.id == "API":
        return arg.attr
    return None


def string_values_of(expr):
    """Return the set of literal strings an expression can evaluate to.

    Handles  'abc'  and  'a' if cond else 'b'  (an "IfExp").  Anything else
    (a call, a variable, an f-string) returns an empty set.
    """
    if isinstance(expr, ast.Constant) and isinstance(expr.value, str):
        return {expr.value}
    if isinstance(expr, ast.IfExp):
        return string_values_of(expr.body) | string_values_of(expr.orelse)
    return set()


def local_string_candidates(scope_node, var_name):
    """Find every literal string assigned to variable var_name in a scope.

    Used when GAM writes   function = 'update' ; callGAPI(svc, function, ...)
    so that we can still check 'update' even though the method name is held
    in a variable.  Also reads parameter default values:  def f(function='get').
    Returns a set of strings (possibly empty = could not tell).
    """
    found = set()
    for node in ast.walk(scope_node):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == var_name:
                    found |= string_values_of(node.value)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = node.args
            # defaults line up with the LAST len(defaults) positional args
            positional = args.args
            for arg, default in zip(positional[len(positional) - len(args.defaults):],
                                    args.defaults):
                if arg.arg == var_name:
                    found |= string_values_of(default)
    return found


def callee_name(call):
    """Return the plain function name of a Call (foo(...) -> 'foo'), else None."""
    if isinstance(call.func, ast.Name):
        return call.func.id
    return None


def collect_scope_maps(tree):
    """Build  {scope name: {variable: set of (API constant, resource path)}}.

    A "scope" is one top level function (including everything nested inside
    it) or one class method.  Module level code is the scope '<module>', which
    is also used as a fallback for every function.

    Two kinds of assignment are recognised:

      1. A builder call:        cd = buildGAPIObject(API.DIRECTORY)
         -> variable 'cd' is (DIRECTORY, path=())      (the service root)

      2. A stored resource chain:   service = cd.orgunits()
         -> variable 'service' is (DIRECTORY, path=('orgunits',))
         (GAM does this a lot, then later calls callGAPI(service, 'list'))

    Kind 2 depends on kind 1, and chains can build on chains, so we repeat the
    scan a few times until nothing new is learned (a "fixed point").
    """
    scopes = defaultdict(lambda: defaultdict(set))

    def targets_of(assign_node):
        """All plain variable names on the left of an assignment."""
        names = []
        for target in assign_node.targets:
            for sub in ast.walk(target):
                if isinstance(sub, ast.Name):
                    names.append(sub.id)
        return names

    def record(scope_name, body_node):
        """One scan over body_node.  Returns True if anything new was learned."""
        learned = False
        for node in ast.walk(body_node):
            if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Call) \
                    and not isinstance(node.value, ast.Name):
                continue
            value = node.value
            # Kind 1: builder call
            if isinstance(value, ast.Call) and callee_name(value) in BUILDERS:
                const = api_constant_from_arg(value, BUILDERS[callee_name(value)])
                if const is None:
                    continue
                entry = (const, ())
                for name in targets_of(node):
                    if entry not in scopes[scope_name][name]:
                        scopes[scope_name][name].add(entry)
                        learned = True
                continue
            # Kind 2: stored chain  service = known_var.res().res2()
            chain = attr_chain(value) if isinstance(value, ast.Call) else None
            if chain and chain[1]:
                var, resources = chain
                known = set(scopes[scope_name].get(var, ())) | \
                    set(scopes["<module>"].get(var, ()))
                for const, base in known:
                    entry = (const, tuple(base) + tuple(resources))
                    for name in targets_of(node):
                        if entry not in scopes[scope_name][name]:
                            scopes[scope_name][name].add(entry)
                            learned = True
        return learned

    def all_scopes():
        """Yield (scope name, node) for every scope in the file."""
        for top in tree.body:
            if isinstance(top, (ast.FunctionDef, ast.AsyncFunctionDef)):
                yield top.name, top
            elif isinstance(top, ast.ClassDef):
                for item in top.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        yield top.name + "." + item.name, item
            else:
                yield "<module>", top

    # ---- Kind 3: parameters.  def helper(drive, ...)  called as helper(drive)
    # We index every function definition by name, then for each call to such a
    # function we copy what we know about the ARGUMENT onto the PARAMETER.
    # This is what lets us see through GAM's many small helper functions.
    function_defs = defaultdict(list)       # name -> [(scope, FunctionDef)]
    for scope_name, scope_node in all_scopes():
        for sub in ast.walk(scope_node):
            if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_defs[sub.name].append((scope_name, sub))

    def entries_for(scope_name, expr):
        """What (API, path) pairs could this call argument expression be?"""
        found = set()
        if isinstance(expr, ast.Name):
            found |= scopes[scope_name].get(expr.id, set())
            found |= scopes["<module>"].get(expr.id, set())
        elif isinstance(expr, ast.Call):
            chain = attr_chain(expr)
            if chain and chain[1]:
                for const, base in entries_for(scope_name, ast.Name(id=chain[0])):
                    found.add((const, tuple(base) + tuple(chain[1])))
        return found

    def propagate_parameters():
        """One pass of argument -> parameter copying.  True if learned more."""
        learned = False
        for caller_scope, caller_node in all_scopes():
            for call in ast.walk(caller_node):
                if not isinstance(call, ast.Call):
                    continue
                fname = callee_name(call)
                if fname is None or fname not in function_defs:
                    continue
                for callee_scope, fdef in function_defs[fname]:
                    params = [a.arg for a in fdef.args.args]
                    pairs = list(zip(params, call.args))
                    pairs += [(kw.arg, kw.value) for kw in call.keywords
                              if kw.arg in params]
                    for param, argument in pairs:
                        for entry in entries_for(caller_scope, argument):
                            if entry not in scopes[callee_scope][param]:
                                scopes[callee_scope][param].add(entry)
                                learned = True
        return learned

    for _ in range(8):                       # a handful of passes is plenty
        progress = False
        for name, node in all_scopes():
            progress |= record(name, node)
        progress |= propagate_parameters()
        if not progress:
            break
    return scopes


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    gam_src, cache_dir, report_dir = sys.argv[1:4]
    os.makedirs(report_dir, exist_ok=True)

    glapi = load_glapi(gam_src)
    index = load_discovery_index(cache_dir)
    load_local_json_docs(gam_src, index)

    # API constant name ('DIRECTORY') -> glapi string ('directory') -> real
    # Google API + version ('admin', 'directory_v1') -> discovery index entry.
    const_to_key = {}
    for const in dir(glapi):
        value = getattr(glapi, const)
        if isinstance(value, str) and value in glapi._INFO:
            cfg = glapi._INFO[value]
            const_to_key[const] = (cfg.get("mappedAPI", value), cfg["version"])

    # Parse GAM's main source file once.
    main_file = os.path.join(gam_src, "gam", "__init__.py")
    with open(main_file, encoding="utf-8") as handle:
        source = handle.read()
    tree = ast.parse(source, filename=main_file)
    scopes = collect_scope_maps(tree)
    module_scope = scopes.get("<module>", {})

    # Results
    missing = []              # strictly resolved calls whose method is missing
    missing_resource = []     # strictly resolved calls whose resource is missing
    loose_missing = []        # unresolved calls found in NO api at all
    not_analyzable = []       # method name is a variable we cannot resolve
    bad_params = []           # keyword arguments Google's method does not accept
    missing_required = []     # required parameters the call never supplies
    stray_positional = []     # extra positional args that land in a wrapper option
    stats = defaultdict(int)  # counters for the summary
    used = defaultdict(set)   # (api,version) -> {'res/path.method'} GAM calls
                              # (STRICT: the variable's API was resolved)
    used_loose = defaultdict(set)   # same, but only matched by name in loose mode
                                    # (may be attributed to several APIs)

    def check(scope_name, line, var, resources, method, via, kwargs=(), splat=True):
        """Check one API call and record the outcome."""
        if method in CLIENT_BUILTINS:
            return
        # googleapiclient auto-generates helper methods that are NOT in the
        # discovery document: 'get_media' (download bytes of 'get'),
        # 'export_media' (download of 'export') and 'list_next' (next page of
        # 'list').  Map each helper back to the real method it wraps.
        for helper_suffix in ("_media", "_next"):
            if method.endswith(helper_suffix) and len(method) > len(helper_suffix):
                method = method[: -len(helper_suffix)]
                break
        method = method.rstrip("_") if method.endswith("_") else method
        # Which API(s) + base resource path could this variable be?  Each
        # candidate is ((real api, version), full resource path string).
        candidates = set()
        for scope_dict in (scopes.get(scope_name, {}), module_scope):
            for const, base in scope_dict.get(var, ()):
                if const in const_to_key:
                    full = "/".join(list(base) + list(resources))
                    candidates.add((const_to_key[const], full))
        path = "/".join(resources)
        # A name that is itself a SUB-RESOURCE (e.g. 'customers' under
        # 'accounts') is just GAM storing a chain such as
        #     service = cchan.accounts().customers()
        # It is not a method call, so there is nothing to verify.
        for key_, full_ in candidates:
            if (full_ + "/" + method).lstrip("/") in index.get(key_, {}):
                stats["resource_accessors_skipped"] += 1
                return
        if candidates:
            stats["resolved"] += 1
            found = False
            resource_exists = False
            allowed = set()           # parameter names valid for this method
            required_sets = []        # required-name set for each matching method
            for key, full in candidates:
                table = index.get(key)
                if table is None:
                    continue          # legacy / local-json API, cannot check
                if full in table:
                    resource_exists = True
                if method in table.get(full, ()):
                    found = True
                    used[key].add("%s.%s" % (full, method))
                    allowed |= PARAMS.get((key, full, method), set())
                    required_sets.append(REQUIRED.get((key, full, method), set()))
            if found and not splat and required_sets:
                # Only judged when the call has no **splat (otherwise the
                # missing name may arrive through the splat at run time).
                # If several candidate methods exist, report only what is
                # missing for EVERY one of them.
                miss = min((r - set(kwargs) for r in required_sets), key=len)
                stats["calls_required_params_checked"] += 1
                if miss:
                    missing_required.append({
                        "line": line, "scope": scope_name, "var": var,
                        "apis": sorted("%s %s /%s" % (k[0], k[1], f)
                                       for k, f in candidates),
                        "path": path, "method": method,
                        "missing": sorted(miss), "via": via})
            if found and kwargs:
                stats["calls_with_parameters_checked"] += 1
                bad = sorted(set(kwargs) - allowed)
                if bad:
                    bad_params.append({
                        "line": line, "scope": scope_name, "var": var,
                        "apis": sorted("%s %s /%s" % (k[0], k[1], f)
                                       for k, f in candidates),
                        "path": path, "method": method, "bad": bad,
                        "via": via})
            checkable = any(k in index for k, _ in candidates)
            if not checkable:
                stats["resolved_but_no_discovery_doc"] += 1
            elif not found:
                entry = {"line": line, "scope": scope_name, "var": var,
                         "apis": sorted("%s %s /%s" % (k[0], k[1], f)
                                        for k, f in candidates),
                         "path": path, "method": method, "via": via}
                (missing if resource_exists else missing_resource).append(entry)
        else:
            # Loose mode: accept if ANY api has this resource path + method.
            stats["unresolved"] += 1
            # The base path of the variable is unknown, so accept the method
            # on any resource whose path ENDS WITH the visible chain (or on any
            # resource at all when the visible chain is empty).
            hits = []
            for k, t in index.items():
                for res_path, methods in t.items():
                    if method in methods and (
                            not path or res_path == path
                            or res_path.endswith("/" + path)):
                        hits.append((k, res_path))
            if hits:
                stats["unresolved_found_somewhere"] += 1
                if path:   # with an empty path EVERY api 'list' would match
                    for key, res_path in hits:
                        used_loose[key].add("%s.%s" % (res_path, method))
                if kwargs:
                    # Accept a keyword if ANY matching method takes it.
                    allowed = set()
                    for key, res_path in hits:
                        allowed |= PARAMS.get((key, res_path, method), set())
                    stats["calls_with_parameters_checked_loose"] += 1
                    bad = sorted(set(kwargs) - allowed)
                    if bad:
                        bad_params.append({
                            "line": line, "scope": scope_name, "var": var,
                            "apis": ["(unresolved - %d candidate methods)" % len(hits)],
                            "path": path, "method": method, "bad": bad,
                            "via": via})
            else:
                loose_missing.append({"line": line, "scope": scope_name,
                                      "var": var, "path": path,
                                      "method": method, "via": via})

    # Walk every function and examine every Call node inside it.
    def examine(scope_name, node_root):
        # --- Pass 1: find call nodes that are merely a LINK in a longer chain.
        # In  iam.projects().serviceAccounts().keys().list(...)  the nodes
        # projects(), serviceAccounts() and keys() are resource names, not
        # methods.  Only the outermost call (list) is a real method call.
        # We collect the ids of the inner links so pass 2 can skip them.
        intermediate = set()
        for node in ast.walk(node_root):
            if not isinstance(node, ast.Call):
                continue
            if (callee_name(node) in WRAPPERS or callee_name(node) == "getattr") \
                    and node.args:
                # first argument of callGAPI/getattr is a chain of resource()
                # calls, i.e. not a method call itself
                intermediate.add(id(node.args[0]))
            if isinstance(node.func, ast.Attribute) \
                    and isinstance(node.func.value, ast.Call) \
                    and node.func.attr not in ("execute", "next_chunk"):
                intermediate.add(id(node.func.value))
        # --- Pass 2: examine the real calls.
        for node in ast.walk(node_root):
            if not isinstance(node, ast.Call):
                continue
            if id(node) in intermediate:
                continue
            name = callee_name(node)
            # Stray positional arguments (see MAX_POSITIONAL above).
            if name in MAX_POSITIONAL and len(node.args) > MAX_POSITIONAL[name]:
                stray_positional.append({
                    "line": node.lineno, "scope": scope_name, "wrapper": name,
                    "extra": [ast.unparse(a)[:40]
                              for a in node.args[MAX_POSITIONAL[name]:]]})
            # Shape A: callGAPI(<chain>, 'method', ...)
            if name in WRAPPERS and len(node.args) >= 2:
                chain = attr_chain(node.args[0])
                method_node = node.args[1]
                if chain and isinstance(method_node, ast.Constant) \
                        and isinstance(method_node.value, str):
                    stats["wrapper_calls_checked"] += 1
                    check(scope_name, node.lineno, chain[0], chain[1],
                          method_node.value, name,
                          splat=any(kw.arg is None for kw in node.keywords),
                          kwargs={kw.arg for kw in node.keywords
                                  if kw.arg and kw.arg not in WRAPPER_OWN_KWARGS
                                  # 'items' is consumed by the paging wrappers
                                  # (callGAPIpages/yieldGAPIpages/callGAPIitems)
                                  # but IS forwarded to Google by plain callGAPI.
                                  and not (kw.arg == "items" and name != "callGAPI")})
                elif chain and isinstance(method_node, ast.Name):
                    # Method name is held in a variable: try to learn its
                    # possible values from literal assignments in this scope.
                    candidates_ = local_string_candidates(node_root, method_node.id)
                    if candidates_:
                        stats["wrapper_calls_dynamic_resolved"] += 1
                        for cand in sorted(candidates_):
                            check(scope_name, node.lineno, chain[0], chain[1],
                                  cand, name + "(dynamic)")
                    else:
                        stats["wrapper_calls_not_analyzable"] += 1
                        not_analyzable.append(
                            {"line": node.lineno, "scope": scope_name,
                             "service": ast.unparse(node.args[0])[:60],
                             "method_variable": method_node.id})
                else:
                    stats["wrapper_calls_not_analyzable"] += 1
                continue
            # Shape C: getattr(<chain>, 'method')  - GAM uses this to pick a
            # method object once and reuse it for batch requests.
            if name == "getattr" and len(node.args) == 2:
                chain = attr_chain(node.args[0])
                method_node = node.args[1]
                if chain and isinstance(method_node, ast.Constant) \
                        and isinstance(method_node.value, str):
                    stats["getattr_calls_checked"] += 1
                    check(scope_name, node.lineno, chain[0], chain[1],
                          method_node.value, "getattr")
                continue
            # Shape B: <chain>.method(...)  where chain has >=1 resource call
            if isinstance(node.func, ast.Attribute):
                chain = attr_chain(node.func.value)
                if chain and chain[1] and (
                        chain[0] in scopes.get(scope_name, {})
                        or chain[0] in module_scope):
                    stats["direct_calls_checked"] += 1
                    check(scope_name, node.lineno, chain[0], chain[1],
                          node.func.attr, "direct",
                          splat=any(kw.arg is None for kw in node.keywords),
                          kwargs={kw.arg for kw in node.keywords if kw.arg})

    for top in tree.body:
        if isinstance(top, (ast.FunctionDef, ast.AsyncFunctionDef)):
            examine(top.name, top)
        elif isinstance(top, ast.ClassDef):
            for item in top.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    examine(top.name + "." + item.name, item)
        else:
            examine("<module>", top)

    # ------------------------------------------------------------------
    # Write the reports (JSON for machines, text for humans).
    # ------------------------------------------------------------------
    # Findings that came from a method name held in a variable are only
    # "possible" problems: the variable may hold different values on different
    # code paths (e.g. 'insert' for messages but 'create' for drafts), and we
    # merge all of them.  Split them out so they are not reported as certain.
    possible = [r for r in missing if r["via"].endswith("(dynamic)")]
    missing = [r for r in missing if not r["via"].endswith("(dynamic)")]
    result = {
        "stats": dict(stats),
        "possible_dynamic_mismatch_verify_manually": possible,
        "bad_parameters": bad_params,
        "missing_required_parameters": missing_required,
        "stray_positional_arguments": stray_positional,
        "missing_method": missing,
        "missing_resource": missing_resource,
        "unresolved_not_found_anywhere": loose_missing,
        "dynamic_method_needs_manual_review": not_analyzable,
        "methods_used_by_gam": {
            "%s %s" % k: sorted(v) for k, v in sorted(used.items())},
        "methods_used_loose_match": {
            "%s %s" % k: sorted(v) for k, v in sorted(used_loose.items())},
    }
    with open(os.path.join(report_dir, "method_audit.json"), "w",
              encoding="utf-8") as handle:
        json.dump(result, handle, indent=1, sort_keys=True)

    lines = []
    lines.append("GAM7 API METHOD AUDIT")
    lines.append("=" * 60)
    for key in sorted(stats):
        lines.append("%-40s %d" % (key, stats[key]))
    for title, rows in (
            ("METHOD MISSING FROM RESOURCE (will crash when run)", missing),
            ("RESOURCE MISSING FROM API (will crash when run)", missing_resource),
            ("DYNAMIC (method held in a variable) - VERIFY MANUALLY, often a false positive", possible),
            ("UNRESOLVED CALLS FOUND IN NO API AT ALL", loose_missing)):
        lines.append("")
        lines.append("%s: %d" % (title, len(rows)))
        lines.append("-" * 60)
        for row in rows:
            lines.append("  line %-6s in %-40s %s -> %s.%s" % (
                row["line"], row["scope"], row.get("apis", row["var"]),
                row["path"], row["method"]))
    lines.append("")
    lines.append("KEYWORD ARGUMENTS GOOGLE DOES NOT ACCEPT (TypeError at run time): %d" % len(bad_params))
    lines.append("-" * 60)
    for row in bad_params:
        lines.append("  line %-6s in %-34s %s.%s  bad=%s  (%s)" % (
            row["line"], row["scope"], row["path"], row["method"],
            ",".join(row["bad"]), "; ".join(row["apis"])[:90]))
    lines.append("")
    lines.append("REQUIRED PARAMETERS NEVER SUPPLIED (TypeError at run time): %d" % len(missing_required))
    lines.append("-" * 60)
    for row in missing_required:
        lines.append("  line %-6s in %-34s %s.%s  missing=%s  (%s)" % (
            row["line"], row["scope"], row["path"], row["method"],
            ",".join(row["missing"]), "; ".join(row["apis"])[:90]))
    lines.append("")
    lines.append("STRAY POSITIONAL ARGUMENTS (silently change retry options): %d" % len(stray_positional))
    lines.append("-" * 60)
    for row in stray_positional:
        lines.append("  line %-6s in %-34s %s(... extra positional: %s)" % (
            row["line"], row["scope"], row["wrapper"], ", ".join(row["extra"])))
    lines.append("")
    lines.append("DYNAMIC METHOD NAMES NEEDING MANUAL REVIEW: %d" % len(not_analyzable))
    lines.append("-" * 60)
    for row in not_analyzable:
        lines.append("  line %-6s in %-40s %s  (method in variable '%s')" % (
            row["line"], row["scope"], row["service"], row["method_variable"]))
    text = "\n".join(lines) + "\n"
    with open(os.path.join(report_dir, "method_audit.txt"), "w",
              encoding="utf-8") as handle:
        handle.write(text)
    print(text)
    return 1 if (missing or missing_resource or bad_params or missing_required) else 0


if __name__ == "__main__":
    sys.exit(main())
