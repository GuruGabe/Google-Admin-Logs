#!/usr/bin/env bash
# =============================================================================
# run_all_audits.sh   (Linux / macOS version - TESTED on Linux 11-21-2026)
#
# PURPOSE
#   Runs every audit tool in the GAM7-Review folder in the right order and
#   writes all reports into one dated folder.  The Windows equivalent is
#   Run-All-Audits.bat in this same folder.
#
# USAGE
#   ./run_all_audits.sh <GAM-src-folder> <python-with-GAM-installed>
#
#   <GAM-src-folder>            the "src" folder of a GAM source checkout, i.e.
#                               the folder that CONTAINS the "gam" folder.
#   <python-with-GAM-installed> a Python interpreter from a virtual environment
#                               in which GAM was installed (needed by tools 03
#                               and 04, which import GAM to inspect it).
#
#   Example:
#     python3 -m venv ~/gamvenv
#     ~/gamvenv/bin/pip install /path/to/GAM
#     ./run_all_audits.sh /path/to/GAM/src ~/gamvenv/bin/python
#
# EXIT CODE
#   0 = every audit finished and found nothing wrong
#   1 = at least one audit reported findings (read the reports)
#   2 = bad arguments or a tool crashed
# =============================================================================

# 'set -u' makes the script stop if it uses a variable that was never set
# (catches typos).  We do NOT use 'set -e' because audit tools intentionally
# exit with 1 when they find problems, and we want to keep going.
set -u

# ---- 1. Check the arguments -------------------------------------------------
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <GAM-src-folder> <python-with-GAM-installed>"
  exit 2
fi
GAM_SRC="$1"
GAM_PY="$2"

# The folder this script lives in, and the review folder one level up.
HERE="$(cd "$(dirname "$0")" && pwd)"
REVIEW="$(cd "$HERE/.." && pwd)"

# A GAM source folder must contain gam/__init__.py - refuse anything else so
# the tools are never pointed at the wrong place.
if [ ! -f "$GAM_SRC/gam/__init__.py" ]; then
  echo "ERROR: $GAM_SRC/gam/__init__.py not found - is that the GAM 'src' folder?"
  exit 2
fi
if [ ! -x "$GAM_PY" ]; then
  echo "ERROR: $GAM_PY is not an executable Python interpreter"
  exit 2
fi

# ---- 2. Make a dated output folder (MM-DD-YYYY_HH-MM) -----------------------
STAMP="$(date +%m-%d-%Y_%H-%M)"
OUT="$REVIEW/09-Reports/run-$STAMP"
CACHE="$OUT/discovery_cache"
mkdir -p "$CACHE"
echo "Reports will be written to: $OUT"

# 'worst' remembers the most serious exit code seen so far.
worst=0
run_step() {
  # run_step "<title>" <command...>   - runs a command, logs its output, and
  # records whether it found problems (1) or crashed (>=2).
  local title="$1"; shift
  echo
  echo "=== $title"
  "$@"
  local rc=$?
  echo "    exit code: $rc"
  if [ "$rc" -gt "$worst" ]; then worst=$rc; fi
}

# ---- 3. Run the tools -------------------------------------------------------
# 'python3 -I' = isolated mode: ignores PYTHON* environment variables and the
# current directory, so a stray file cannot hijack 'import json' etc.
run_step "01 Fetch Google discovery documents" \
  python3 -I "$REVIEW/01-Discovery-Fetch/fetch_discovery.py" "$GAM_SRC" "$CACHE"

run_step "02 API method / parameter audit" \
  python3 -I "$REVIEW/02-API-Method-Audit/audit_api_methods.py" "$GAM_SRC" "$CACHE" "$OUT"

run_step "03 Constant reference audit" \
  "$GAM_PY" "$REVIEW/03-Constant-Reference-Audit/audit_constant_references.py" "$GAM_SRC" "$OUT"

run_step "04 Message format audit" \
  "$GAM_PY" "$REVIEW/04-Message-Format-Audit/audit_message_format.py" "$GAM_SRC" "$OUT"

run_step "05 API coverage / deprecation / currency report" \
  python3 -I "$REVIEW/05-API-Coverage-Gaps/api_coverage_report.py" "$GAM_SRC" "$CACHE" "$OUT/method_audit.json" "$OUT"

run_step "06 OAuth scope audit" \
  python3 -I "$REVIEW/06-OAuth-Scope-Audit/audit_oauth_scopes.py" "$GAM_SRC" "$CACHE" "$OUT"

echo
echo "Finished.  Worst exit code: $worst   (0 clean, 1 findings, 2+ crash)"
echo "Reports: $OUT"
exit "$worst"
