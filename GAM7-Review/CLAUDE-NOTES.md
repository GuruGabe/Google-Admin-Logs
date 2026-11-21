# CLAUDE-NOTES.md - working notes for the assistant (read AND write)

Purpose of this file: so a future session (mine or anyone's) knows exactly
what was done, what is left, and what to try next, without re-deriving it.
Dates are MM-DD-YYYY, times HH:MM (UTC unless stated).

## Task as given (11-21-2026)

The user will be away from work until 11-30-2026 and said I would not have
access to the work computer. They asked me to: thoroughly go through the GAM7
code looking for problems and improvements; do my best to make GAM7
"completely use all of Google's API"; and ensure no running errors when
attempting to run any commands.

User preferences that apply (also in the system prompt): Windows batch first,
PowerShell second, Python last; ASCII only in scripts; comment everything
heavily; explain PowerShell/Python in detail; each script in its own folder;
keep a notes file like this one; always write a how-to document; double-check
for security flaws; dates MM-DD-YYYY, times HH:MM.

## State at end of session 1 (11-21-2026, about 04:25)

DONE
* Cloned upstream GAM (GAM-team/GAM, read-only, shallow) to
  `/home/user/gam-team/gam` at commit 30449fc = GAM 7.52.05.  (Sandbox path;
  gone when the container is reclaimed. Re-clone with
  `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/GAM-team/GAM`.)
* Built tools 01-06 and 08, runners in 00, reports in 09, patches in 07.
* Ran everything on the pristine upstream commit; baseline is
  `09-Reports/run-11-21-2026_04-14/`.
* Found and fixed 2 real crash bugs (patch 0001) and made 2 hardening
  changes (patch 0002).  See FINDINGS-11-21-2026.md.
* Mutation-tested the audit tool (4 seeded defects, all caught).
* pip-audit on pinned dependencies: clean.  bandit: 4 hits triaged (2 fixed in
  0002, 2 safe).  Python 3.10 grammar check: clean.  vermin: min 3.10.

NOT DONE (explicit)
* No new GAM commands/APIs implemented (see "Ideas").
* Nothing run against a real Google tenant (no credentials).
* `Run-All-Audits.bat` never executed (Linux sandbox). Test on Windows.
* GAMGUI (`GuruGabe/GAM-GUI-Overlay`) not reviewed.
* `Admin-Logs.bat` in the repo root (user's own script) not reviewed - it was
  not part of the request.
* Could not read developers.google.com (blocked by sandbox network policy), so
  Email Audit API / Contacts v3 status is unverified.
* Patches not offered upstream: add_repo(push) on GAM-team/GAM was refused (no
  write access). Ready-to-paste issue text is in 10-Upstream-Issue-Drafts/;
  the user posts them, or forks and sends a PR with 07-Patches.

## Where things live

Repo: GuruGabe/Google-Admin-Logs, branch `claude/gam7-review-api-acys4n`
(develop and push only there; do NOT open a PR unless the user asks).
Only `Admin-Logs.bat` existed at repo root before this work.

## Key technical facts learned (so they need not be rediscovered)

* GAM builds its API clients at run time from Google discovery documents;
  `glapi._INFO` maps GAM's internal names to (api, version, v2discovery,
  mappedAPI, localjson).  v2discovery URL:
  `https://<api>.googleapis.com/$discovery/rest?version=<ver>`; v1 URL:
  `https://www.googleapis.com/discovery/v1/apis/<api>/<ver>/rest`.
* `glapi.py` has no imports, so tools load it by file path with importlib
  instead of importing the `gam` package (which pulls in everything).
* googleapiclient rejects unknown keyword args with
  `TypeError: Got an unexpected keyword argument X`; GAM's `callGAPI*` forward
  everything except its own wrapper kwargs (`WRAPPER_OWN_KWARGS` in tool 02;
  `items` is consumed by callGAPIpages/yieldGAPIpages/callGAPIitems only).
* googleapiclient generates `*_media` and `*_next` helpers and appends `_` to
  Python keywords (`import` -> `import_`); tool 02 normalises these.
* GAM wrappers: callGAPI, callGAPIpages, yieldGAPIpages, callGAPIitems; direct
  calls and `getattr(chain, 'method')` also exist.  Chains are often stored in
  variables (`service = cc.accounts().customers()`) and service objects are
  passed through helper functions; tool 02 propagates both (fixed-point).
* Coverage counts in tool 05 are LOWER BOUNDS (data-driven resource tables).
* `iam v2` only has the `policies` resource, so GAM correctly uses `iam v1`.
* Four scopes are valid but missing from Google's docs (see KNOWN_DOC_GAPS in
  tool 06).  `apps.order.readonly` for Cloud Channel is the one open question.

## Work log - proofs worth keeping

Bug 1 proof (real googleapiclient + Google's Vault doc):
`vault.matters().holds().update(throwReas=[1], matterId='m', holdId='h', body={})`
-> `TypeError: Got an unexpected keyword argument throwReas`.

Bug 2 proof:
`croom.courses().students().delete(courseId='c', body={...}, fields='')`
-> `TypeError: Got an unexpected keyword argument body`; the fixed shape
`delete(courseId='c', userId='u', fields='')` builds
`DELETE https://classroom.googleapis.com/v1/courses/c/students/u?fields=&alt=json`.
Through GAM's own callGAPI with a mocked HTTP answer the old shape aborts with
`ERROR: Got an unexpected keyword argument body`; the new shape returns `{}`.

Mistakes I made and corrected on the way (do not repeat):
* First version of tool 02 flagged ~300 "missing methods" - it treated the
  intermediate links of a chain (`.projects().serviceAccounts()`) as method
  calls, and did not know `yieldGAPIpages`, stored chains, `get_media`,
  `list_next`, `import_`.  Fixed, and a mutation test now guards it.
* Tool 05 first reported Analytics `conversionEvents` and Drive `teamdrives`
  as deprecated methods GAM calls.  Cause: my loose matching treated an empty
  resource path as "any API's `list`".  Fixed (empty path never counts);
  verified by grep that GAM does not call them.
* I saved Google's API directory with `?preferred=true` once, which hid older
  versions and produced fake "version not in directory" rows.  The tool now
  expects the full directory (`https://www.googleapis.com/discovery/v1/apis`).

## Session 2 (11-21-2026, later)

* User created fork GuruGabe/GAM and linked GitHub. Fork cloned at
  /home/user/gam; branch `claude/gam7-audit-fixes` (2 commits = patches 0001,
  0002) pushed to the fork. No PR opened yet (user to decide: 1 or 2 PRs).
* GAM-team/GAM write access is impossible for this session (add_repo push
  refused), so issues cannot be posted by me. Built `10-Upstream-Issue-Drafts/`
  (4 drafts + LINKS.md with pre-filled new-issue URLs) for the user to submit.
* New checks: stray positional args (in tool 02), dict-built kwargs (15 sites,
  clean; one-off, not yet a tool), paged `items` names (tool 11; 217 checked,
  clean; mutation-tested).  Resolved most of the 23 dynamic call sites by
  hand: all valid (`getContactPhoto` is not called through callGAPI;
  `trash/untrash` only exist as a function value that is never reached).
* NEXT hunting ideas: turn the dict-kwargs check into a tool; check
  throwReasons names against GAPI exception map; check `fields=` strings
  against response schemas; check wiki command syntax vs parser.

## Session 2b (11-21-2026, later still)

* Added tool 12 (fields masks; mutation-tested) and patch 0003 (name(fullName));
  fork branch claude/gam7-audit-fixes now has 3 commits (pushed).
* issue-5 draft + LINKS.md regenerate needed whenever drafts change (script in
  session history: percent-encode title/body into
  https://github.com/GAM-team/GAM/issues/new?title=..&body=..).
* Throw-vs-catch check is only a LEAD (09-Reports/throw-vs-catch-leads...):
  ProcessGAMCommand prints a traceback for uncaught GAPI errors except
  permissionDenied/accessNotConfigured, but GAM remaps raw reasons in
  checkGAPIError, so real impact needs live testing.
* Test harness trick (callGAPI without credentials): build a client with
  googleapiclient.discovery.build_from_document + HttpMockSequence, then set
  gam.GM.Globals[EXTRA_ARGS_LIST]=[] and gam.GC.Values.update({API_CALLS_RATE_CHECK:False,
  RETRY_API_SERVICE_NOT_AVAILABLE:False, API_CALLS_TRIES_LIMIT:3,
  BAIL_ON_INTERNAL_ERROR_TRIES:2, DEBUG_LEVEL:0}).

## Session 2c (11-21-2026, later still)

* The USER MERGED PR #1 on their own fork (GuruGabe/GAM main = 265011f) containing
  patches 0001+0002.  Patch 0003 is still only on claude/gam7-audit-fixes.
  Upstream GAM-team/GAM main was still 30449fc when checked (all 3 patches apply).
* New: tool 13 (wiki links + documented-command check) and fork branch
  claude/gam7-wiki-fixes (docs only; 2 typos + 9 links).  pr-6-wiki-fixes.md has PR text.
* Never repeat personal names seen in git logs in outward text.

* Tool 14 (config table + gam.cfg wiki) added; wiki branch has a 2nd commit (cfg defaults).
  Config tables in code are self-consistent (143 settings, no bad defaults).
  no_update_check is intentionally ignored by GAM (see GamUpdate.txt) - not a bug.

## TODO next (priority order)

1. Ask the user (when they are back, around 11-30-2026):
   a. How is GAM installed at work (packaged installer or source)? That decides
      whether the patches can be applied or must be reported upstream.
   b. Permission to open an issue/PR on GAM-team/GAM for the two bugs
      (needs `add_repo` with push access or the user's own fork).
   c. Whether to review GAMGUI (`GuruGabe/GAM-GUI-Overlay`) and/or
      `Admin-Logs.bat` next.
2. On the work machine (with real credentials, test domain preferably):
   * `gam update vaulthold` on a test hold - confirm the fixed call works.
   * `gam oauth create` and tick the Cloud Channel read-only option - confirm
     whether `apps.order.readonly` is accepted.
   * `gam create monitor ...` (Email Audit) and a domain shared contact
     command - confirm those legacy APIs still answer.
   * Run `Run-All-Audits.bat` once to validate the .bat.
3. Re-run all tools after the next GAM release and diff against the baseline.
4. Resolve the 23 "dynamic method" call sites by hand (listed at the bottom of
   `09-Reports/.../method_audit.txt`); a simple way is to grep what values the
   variable can take at each site.
5. Remove dead legacy code only if upstream agrees (atom/url.py `cmp`, etc.).

## Ideas for improvement (not done)

* New GAM commands, best value for the user's goals (security, user
  experience, troubleshooting), details in
  `09-Reports/candidate-new-apis-11-21-2026.md`:
  1. Gmail Postmaster Tools v2 - domain reputation, spam rate, SPF/DKIM/DMARC.
  2. Workspace Marketplace (appsmarket v2) - installed third-party apps.
  3. Data Portability v1 - user data export for offboarding.
  4. Apps Script v1 - find and review script projects.
  5. Slides v1, Workspace Events v1, Cloud Search v1.
  Any of these needs: discovery document, scope table entries in `glapi.py`
  (`_INFO`, `_CLIENT_SCOPES`, `_SVCACCT_SCOPES`), command parser, help text,
  and testing on a real tenant.  Follow GAM's existing patterns.
* Make tool 02 interprocedural for method names (the 23 dynamic sites) and for
  required parameters passed through `svcargs` dictionaries.
* Add a CI-style check: run the tools in GitHub Actions weekly and open an
  issue when a finding appears (Google changes APIs without notice).
* A small PowerShell wrapper around the runner for users who prefer it.
* A tool that tests GAM end to end against a fake local Google server
  (mock discovery + canned JSON) to exercise argument parsing for every
  command without credentials.  That would be the next real step towards
  "no running errors for any command".

## Environment gotchas (sandbox)

* Outbound HTTPS only via the agent proxy; googleapis.com, pypi.org and github
  worked; developers.google.com was refused (403).  Do not change network
  settings unless the user asks.
* `gam checkconn` fails here on TLS (proxy CA) - not a GAM bug.
* The Bash tool resets the working directory after every call; use absolute
  paths.
