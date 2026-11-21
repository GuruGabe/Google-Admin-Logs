@echo off
REM ============================================================================
REM Run-All-Audits.bat   (Windows version)
REM
REM NOTE: written 11-21-2026 on a Linux machine.  The shell twin of this file
REM       (run_all_audits.sh) was run and tested; this .bat file could NOT be
REM       executed there, so test it once before relying on it.
REM
REM PURPOSE
REM   Runs every audit tool in the GAM7-Review folder, in order, and writes all
REM   reports into one dated folder under 09-Reports.
REM
REM USAGE
REM   Run-All-Audits.bat "<GAM src folder>" "<python.exe that has GAM installed>"
REM
REM   Argument 1: the "src" folder of a GAM source checkout - the folder that
REM               CONTAINS the "gam" folder.
REM               Example: "C:\GAM-source\GAM\src"
REM   Argument 2: python.exe from a virtual environment where GAM was
REM               installed (tools 03 and 04 import GAM, so they need GAM's
REM               libraries).  Example: "C:\gamvenv\Scripts\python.exe"
REM
REM   One-time setup example (run in a normal Command Prompt):
REM     python -m venv C:\gamvenv
REM     C:\gamvenv\Scripts\pip install C:\GAM-source\GAM
REM
REM EXIT CODE
REM   0 = all audits clean, 1 = findings were reported, 2 = bad input or crash
REM ============================================================================

REM setlocal keeps every variable we create private to this script, so nothing
REM leaks into your Command Prompt session.  EnableExtensions turns on the
REM modern forms of IF and FOR that this file uses.
setlocal EnableExtensions

REM ---- 1. Check arguments ----------------------------------------------------
REM %~1 is argument 1 with any surrounding quotes removed; "%~1"=="" is true if
REM the argument is missing.
if "%~1"=="" goto :usage
if "%~2"=="" goto :usage
set "GAM_SRC=%~1"
set "GAM_PY=%~2"

REM The GAM source folder must contain gam\__init__.py.  Refusing anything else
REM prevents running the tools against the wrong folder.
if not exist "%GAM_SRC%\gam\__init__.py" (
  echo ERROR: "%GAM_SRC%\gam\__init__.py" was not found.
  echo        Is the first argument the GAM "src" folder?
  exit /b 2
)
if not exist "%GAM_PY%" (
  echo ERROR: "%GAM_PY%" was not found.
  exit /b 2
)

REM ---- 2. Locate the review folder (the parent of this script's folder) ------
REM %~dp0 is the folder this .bat lives in, with a trailing backslash.
REM The FOR loop converts "<folder>\.." into a clean absolute path.
for %%I in ("%~dp0..") do set "REVIEW=%%~fI"

REM ---- 3. Build a locale-proof timestamp MM-DD-YYYY_HH-MM --------------------
REM %DATE% and %TIME% change format with the Windows region settings, so we ask
REM PowerShell for the exact text instead.  -NoProfile skips the user's
REM PowerShell profile so nothing unexpected runs.
set "STAMP="
for /f "usebackq delims=" %%T in (`powershell -NoProfile -Command "Get-Date -Format 'MM-dd-yyyy_HH-mm'"`) do set "STAMP=%%T"
if "%STAMP%"=="" set "STAMP=unknown-time"

set "OUT=%REVIEW%\09-Reports\run-%STAMP%"
set "CACHE=%OUT%\discovery_cache"
if not exist "%CACHE%" mkdir "%CACHE%"
echo Reports will be written to: %OUT%

REM WORST remembers the highest exit code any tool returned.
set "WORST=0"

REM ---- 4. Run the tools ------------------------------------------------------
REM "python -I" = isolated mode: ignores PYTHON* environment variables and the
REM current folder, so a stray file cannot replace a standard module.
REM Each step: run the tool, grab its exit code (%ERRORLEVEL%), and update WORST.

echo.
echo === 01 Fetch Google discovery documents
python -I "%REVIEW%\01-Discovery-Fetch\fetch_discovery.py" "%GAM_SRC%" "%CACHE%"
call :track

echo.
echo === 02 API method and parameter audit
python -I "%REVIEW%\02-API-Method-Audit\audit_api_methods.py" "%GAM_SRC%" "%CACHE%" "%OUT%"
call :track

echo.
echo === 03 Constant reference audit
"%GAM_PY%" "%REVIEW%\03-Constant-Reference-Audit\audit_constant_references.py" "%GAM_SRC%" "%OUT%"
call :track

echo.
echo === 04 Message format audit
"%GAM_PY%" "%REVIEW%\04-Message-Format-Audit\audit_message_format.py" "%GAM_SRC%" "%OUT%"
call :track

echo.
echo === 05 API coverage, deprecation and currency report
python -I "%REVIEW%\05-API-Coverage-Gaps\api_coverage_report.py" "%GAM_SRC%" "%CACHE%" "%OUT%\method_audit.json" "%OUT%"
call :track

echo.
echo === 06 OAuth scope audit
python -I "%REVIEW%\06-OAuth-Scope-Audit\audit_oauth_scopes.py" "%GAM_SRC%" "%CACHE%" "%OUT%"
call :track

echo.
echo === 11 Paged-items audit (silent empty-result bugs)
python -I "%REVIEW%\11-Paged-Items-Audit\audit_paged_items.py" "%GAM_SRC%" "%CACHE%"
call :track

echo.
echo Finished.  Worst exit code: %WORST%   (0 clean, 1 findings, 2+ crash)
echo Reports: %OUT%
exit /b %WORST%

REM ---- Subroutines -----------------------------------------------------------
:track
REM Called right after each tool.  Prints its exit code and keeps the maximum.
REM Inside a subroutine %ERRORLEVEL% still holds the caller's last result.
echo     exit code: %ERRORLEVEL%
if %ERRORLEVEL% GTR %WORST% set "WORST=%ERRORLEVEL%"
goto :eof

:usage
echo Usage: %~nx0 "^<GAM src folder^>" "^<python.exe that has GAM installed^>"
exit /b 2
