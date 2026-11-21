# GAM7 Review Toolkit - How to Use It

Written 11-21-2026. Read `FINDINGS-11-21-2026.md` first for the results; this
file explains how the tools work and how to run them again.

---

## 1. What is in this folder

| Folder / file | What it is |
|---|---|
| `FINDINGS-11-21-2026.md` | The results of the review: bugs, risks, API coverage. Start here. |
| `CLAUDE-NOTES.md` | Working notes for the assistant (what was done, what is left, ideas). Also useful to you as a history. |
| `00-Run-All/` | One-command runners: `Run-All-Audits.bat` (Windows) and `run_all_audits.sh` (Linux/macOS). |
| `01-Discovery-Fetch/` | Downloads Google's description of every API GAM uses. |
| `02-API-Method-Audit/` | The main audit: do the API methods, parameters and resources GAM uses really exist? |
| `03-Constant-Reference-Audit/` | Do all the names GAM uses (`Msg.X`, `Ent.X`, `GAPI.X` ...) exist? |
| `04-Message-Format-Audit/` | Do GAM's message templates get the right number of arguments? |
| `05-API-Coverage-Gaps/` | Which Google methods GAM never calls, deprecated calls, API versions. |
| `06-OAuth-Scope-Audit/` | Do the permission strings (scopes) GAM asks for still exist? |
| `07-Patches/` | Ready-to-apply fixes for GAM (two patch files). |
| `08-Candidate-API-Details/` | Prints an outline of any Google API (for planning new GAM commands). |
| `09-Reports/` | Saved results: the 11-21-2026 baseline run and the candidate-API outline. |
| `10-Upstream-Issue-Drafts/` | Four ready-to-post GitHub issues for GAM-team/GAM, plus `LINKS.md` with one-tap pre-filled links. |
| `11-Paged-Items-Audit/` | Finds list calls that would silently return nothing because a response field name is wrong. |

Every `.py` file has a long comment at the top explaining its purpose and
every step of the code is commented.

---

## 2. The ideas behind the tools (plain English)

**GAM is a program that talks to Google's servers.** Each command ends up
calling an "API method", for example "list the users" or "update a Vault
hold".

**Google publishes a machine-readable description of each API** called a
*discovery document*. It lists every resource, every method, every parameter
and which are required, and which permissions ("OAuth scopes") are needed.
GAM itself downloads these descriptions while it runs and builds its Python
client from them.

**The danger:** if GAM's code uses a method or parameter name that is not in
that description (because of a typo, or because Google renamed or removed
something), Python crashes with an error such as
`Got an unexpected keyword argument` - but only when somebody runs that exact
command, which may be months after the mistake was made.

**The tools** compare GAM's source code with Google's descriptions ahead of
time, so such mistakes are found before a user hits them.

**How the code is read without running it:** Python can turn source code into
an *AST* (abstract syntax tree), a structured outline of the program. The
audit tools use Python's built in `ast` module to ask questions like "show
me every call to `callGAPI`". This is much more reliable than searching the
text, and nothing from GAM is ever executed during the parsing.

---

## 3. One-time setup

You need:

1. **Python 3.10 or newer** (already on any machine where you run GAM from
   source; check with `python --version`).
2. **A copy of the GAM source code.** Get it from
   https://github.com/GAM-team/GAM (green Code button -> Download ZIP, or
   `git clone https://github.com/GAM-team/GAM`). The tools need the folder
   named **`src`** that contains the folder `gam`.
3. **A Python virtual environment with GAM installed** (only tools 03 and 04
   need this, because they import GAM to inspect its real objects).

Windows Command Prompt, step by step:

```
python -m venv C:\gamvenv
C:\gamvenv\Scripts\pip install C:\GAM-source\GAM
```

(`C:\GAM-source\GAM` is wherever you put the downloaded source; it is the
folder that contains `pyproject.toml`.) A "virtual environment" is just a
private folder of Python libraries so installing GAM's libraries does not
touch the rest of your system.

Linux / macOS:

```
python3 -m venv ~/gamvenv
~/gamvenv/bin/pip install /path/to/GAM
```

**Internet access** is needed for tools 01, 05 (anonymous downloads of
Google's public API descriptions only) and 08. No Google login, password or
token is ever needed or sent.

---

## 4. Run everything with one command

Windows:

```
00-Run-All\Run-All-Audits.bat "C:\GAM-source\GAM\src" "C:\gamvenv\Scripts\python.exe"
```

Linux / macOS:

```
00-Run-All/run_all_audits.sh /path/to/GAM/src ~/gamvenv/bin/python
```

* Argument 1 = the GAM `src` folder. Argument 2 = the Python from the virtual
  environment.
* Results go to `09-Reports\run-MM-DD-YYYY_HH-MM\`.
* The last line shows the worst exit code: `0` everything clean, `1` something
  was reported (read the reports), `2` or more = a tool crashed or the
  arguments were wrong.
* Takes about two to three minutes (most of it is downloading).

> Windows note: `Run-All-Audits.bat` was written on a Linux computer and could
> not be executed there. Its Linux twin `run_all_audits.sh` was run and works.
> Please test the `.bat` once; if anything in it misbehaves, run the tools one
> by one as shown in section 5 - that always works.

---

## 5. Running the tools one at a time

All commands below are run from the `GAM7-Review` folder. Replace the paths.
`python -I` means "isolated mode": Python ignores environment variables and
the current folder so a stray file cannot replace a standard module. It is a
security habit worth keeping.

### Tool 01 - download Google's API descriptions

```
python -I 01-Discovery-Fetch\fetch_discovery.py C:\GAM-source\GAM\src C:\work\discovery_cache
```

Reads GAM's own API table (`gam/gamlib/glapi.py`), downloads one description
per API into the cache folder (about 6 MB). Two APIs (`contacts`,
`email-audit`) are reported as `skipped`; that is **expected** - they are old
"GData" APIs that never had a description document.

### Tool 02 - the main audit

```
python -I 02-API-Method-Audit\audit_api_methods.py C:\GAM-source\GAM\src C:\work\discovery_cache C:\work\reports
```

Writes `method_audit.txt` (human readable) and `method_audit.json`.
Sections in the report:

* **METHOD MISSING / RESOURCE MISSING** - GAM calls something Google does not
  have. Will crash. Should be 0.
* **KEYWORD ARGUMENTS GOOGLE DOES NOT ACCEPT** - GAM sends a parameter name
  Google's method does not have (typos!). Will crash. Should be 0.
* **REQUIRED PARAMETERS NEVER SUPPLIED** - a call forgets a parameter Google
  requires. Will crash. Should be 0.
* **DYNAMIC (method held in a variable)** - the method name is chosen at run
  time; the tool merged every possible value, so these are *hints*, often
  false alarms. Look at the code and decide. (The three Gmail entries seen on
  11-21-2026 are false alarms: messages use `import_`/`insert`, drafts use
  `create`.)
* **UNRESOLVED ... FOUND IN NO API AT ALL** - could not tell which API the call
  belongs to, and no API has such a method. (On 11-21-2026 this was one false
  alarm: a plain `getattr(f, 'name')` on a file object.)
* **STRAY POSITIONAL ARGUMENTS** - a call passes more unnamed arguments than
  the GAM wrapper takes, so the extra one silently lands in a retry option.
  Not a crash, but changes behavior (2 found on 11-21-2026).
* **DYNAMIC METHOD NAMES NEEDING MANUAL REVIEW** - 23 call sites where the
  method name cannot be determined statically. A to-do list for a human.

The counters at the top say how much was verified *strictly* (the tool knew
exactly which API) and how much only *loosely* (matched by name). Strict is
stronger evidence.

### Tool 03 - do all the names GAM uses exist? (needs the virtual environment's Python)

```
C:\gamvenv\Scripts\python.exe 03-Constant-Reference-Audit\audit_constant_references.py C:\GAM-source\GAM\src C:\work\reports
```

GAM's code refers to thousands of constants like `Msg.NOT_FOUND`. A
misspelled one only crashes when that line runs. This imports the real
objects and checks every reference. Expected: `Missing references : 0`.

### Tool 04 - message templates (needs the virtual environment's Python)

```
C:\gamvenv\Scripts\python.exe 04-Message-Format-Audit\audit_message_format.py C:\GAM-source\GAM\src C:\work\reports
```

GAM message text such as `'{0} {1} not found'` must receive exactly that many
values. Too few raises an error *inside an error message*, hiding the real
problem. Expected: `Certain crashes : 0`.

### Tool 05 - coverage, deprecations, versions

```
python -I 05-API-Coverage-Gaps\api_coverage_report.py C:\GAM-source\GAM\src C:\work\discovery_cache C:\work\reports\method_audit.json C:\work\reports
```

Run tool 02 first (it needs `method_audit.json`). Writes
`api_coverage_report.md`: per-API coverage, calls to methods Google marks
deprecated, API version currency, Workspace APIs GAM does not use.
**The coverage counts are lower bounds** (see FINDINGS section 4).
The list of "Workspace-relevant APIs" near the top of the script is a
hand-written judgement; edit it freely.

### Tool 06 - OAuth scopes

```
python -I 06-OAuth-Scope-Audit\audit_oauth_scopes.py C:\GAM-source\GAM\src C:\work\discovery_cache C:\work\reports
```

Checks every permission string GAM asks for against Google's list. A scope
that no longer exists makes authorization fail. The tool keeps a short list of
scopes that are valid but missing from Google's documents (each with the
reason). Anything else it prints deserves a look.

### Tool 11 - silent empty-result bugs

```
python -I 11-Paged-Items-Audit\audit_paged_items.py C:\GAM-source\GAM\src C:\work\discovery_cache
```

GAM list commands name the field of Google's answer that holds the list
(`callGAPIpages(cd.users(), 'list', 'users')`). A wrong name does not crash;
the command just prints nothing. This checks every such name against Google's
response description. Expected: `Suspicious items names: 0`.

### Tool 08 - outline of any Google API (for planning new GAM commands)

```
python -I 08-Candidate-API-Details\describe_apis.py outline.md appsmarket script slides
```

Names are Google's API names (list: https://www.googleapis.com/discovery/v1/apis).
Produces a Markdown file listing every method, its URL, required parameters
and scopes.

---

## 6. Applying the fixes in `07-Patches`

Two patch files, to be applied **in order** to a GAM **source** checkout:

```
cd C:\GAM-source\GAM
git apply --check C:\path\to\07-Patches\0001-Fix-two-API-call-crashes-found-by-static-audit.patch
git apply         C:\path\to\07-Patches\0001-Fix-two-API-call-crashes-found-by-static-audit.patch
git apply --check C:\path\to\07-Patches\0002-Harden-gcloud-reauth-SQL-lookup-and-make-Drive-md5-c.patch
git apply         C:\path\to\07-Patches\0002-Harden-gcloud-reauth-SQL-lookup-and-make-Drive-md5-c.patch
```

`--check` only tests whether the patch fits and changes nothing - always run
it first. Both patches were verified against upstream commit `30449fc`; if
GAM has moved on since then they may need adjusting, but each change is only
one or two lines (they are readable in any text editor).

**Important:** most GAM7 installs (the standard installer) are a packaged
program, not source code, and patches only change a source checkout. I do not
know how GAM is installed on your work computer. If it is the packaged kind,
the realistic path is to report the two bugs
to the GAM maintainers (https://github.com/GAM-team/GAM/issues) and update
GAM when they release the fix. Do not post the patches or any report there
without reading them first: they contain only code and public information, but
it is your call.

---

## 7. Keeping this useful over time

* **After every GAM update** run `Run-All-Audits` again and compare with
  `09-Reports\run-11-21-2026_04-14\` (the baseline). New findings are new
  mistakes (or Google changes).
* **Seeing "0 findings" is only meaningful if the tool can find things.** On
  11-21-2026 I tested that by deliberately breaking a scratch copy of GAM in
  four ways; all four were caught. If you change a tool, repeat such a test.
* The tools do **not** replace running GAM against a real test tenant. They
  catch one family of crashes (code that Google's client library rejects
  before sending anything). They cannot see problems that depend on real data.

---

## 8. Security notes about these tools

* Read only: they never change GAM, never run GAM commands, never touch
  credentials (`oauth2.txt`, `client_secrets.json`, service account keys).
* The only network traffic is anonymous HTTPS downloads of Google's public
  API descriptions. TLS certificate checking stays on. Do not turn it off; if
  your network inspects TLS, add your company's certificate to Python instead.
* Tools 03 and 04 import GAM; importing creates the folder `.gam` in your user
  profile with a default `gam.cfg` the first time (GAM does this on its own
  too). Nothing is sent anywhere.
* File and API names taken from data are validated before they are used to
  build file names or URLs.

---

## 9. Glossary

* **API** - the set of "methods" a service offers programs.
* **Discovery document** - Google's machine-readable description of an API.
* **OAuth scope** - a permission string, e.g. `.../auth/admin.directory.user`.
* **AST** - Python's structured outline of source code.
* **Strict / loose** (in the reports) - strict = the tool knew exactly which
  API a call belongs to; loose = matched by method name only.
* **Patch** - a small file that describes exact line changes to code.
* **Exit code** - the number a program returns when it ends; `0` means success.
