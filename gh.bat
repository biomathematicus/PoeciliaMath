@echo off
setlocal enabledelayedexpansion

rem ================================================================
rem  gh.bat  --  Git helper with automatic version stamping
rem
rem  Usage:
rem    gh                    Pull only; print session verification prompt
rem    gh "commit message"   Stage, pull, commit, push, stamp, re-push
rem ================================================================

set TEXFILE=poecilia_manuscript.tex
set VERSIONFILE=VERSION

rem ================================================================
rem  PULL-ONLY MODE  (no arguments)
rem ================================================================
if "%~1"=="" (
    echo [gh] No commit message supplied -- pulling only.
    git pull origin main
    for /f %%i in ('git rev-parse --short HEAD') do set HASH=%%i
    echo [gh] Current HEAD: !HASH!
    call :PRINT_PROMPT
    goto :EOF
)

rem ================================================================
rem  COMMIT MODE
rem ================================================================

rem ---- Stage all changes ----
git add -A

rem ---- Pull before committing to avoid divergence ----
git pull origin main

rem ---- Commit only if there is something staged ----
git diff --cached --quiet
if errorlevel 1 (
    git commit -m %*
) else (
    echo [gh] Nothing to commit -- working tree clean.
)

rem ---- Push ----
git push origin HEAD

rem ---- Capture the hash that is now on the remote ----
for /f %%i in ('git rev-parse --short HEAD') do set HASH=%%i
echo [gh] Pushed commit: !HASH!

rem ================================================================
rem  VERSION STAMP
rem  Write VERSION file and update % GITCOMMIT: in the .tex preamble
rem  then do a second lightweight commit so both artefacts are indexed
rem ================================================================

rem ---- Write VERSION ----
echo !HASH! %DATE% %TIME%> !VERSIONFILE!

rem ---- Update % GITCOMMIT: line in the .tex file (if it exists) ----
if exist !TEXFILE! (
    powershell -NoProfile -Command ^
        "(Get-Content '!TEXFILE!') ^
         -replace 'GITCOMMIT:.*', 'GITCOMMIT: !HASH!' ^
         | Set-Content '!TEXFILE!'"
    echo [gh] Updated GITCOMMIT in !TEXFILE!
) else (
    echo [gh] WARNING: !TEXFILE! not found -- GITCOMMIT line not updated.
)

rem ---- Stage the stamp files ----
git add !VERSIONFILE! !TEXFILE!

rem ---- Second commit only if stamp files actually changed ----
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "Auto: version stamp !HASH!"
    git push origin HEAD
    rem Capture the stamp-commit hash as the canonical session hash
    for /f %%i in ('git rev-parse --short HEAD') do set HASH=%%i
    echo [gh] Version stamp commit: !HASH!
)

rem ---- Print the Claude session prompt ----
call :PRINT_PROMPT
goto :EOF

rem ================================================================
rem  SUBROUTINE: print copy-paste Claude verification prompt
rem ================================================================
:PRINT_PROMPT
echo.
echo =================================================================
echo  CLAUDE SESSION VERIFICATION PROMPT  (copy the block below)
echo =================================================================
echo.
echo   Before evaluating any inputs or producing outputs, search
echo   project knowledge for "GITCOMMIT !HASH!" and confirm that
echo   the search returns a result containing that exact string.
echo   If the search returns an older hash or nothing, the project
echo   knowledge base has not yet re-indexed -- wait ~5 minutes and
echo   run  gh  (pull-only) to get a fresh prompt before proceeding.
echo.
echo   Current commit: !HASH!
echo =================================================================
echo.
goto :EOF