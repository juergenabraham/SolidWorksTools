@echo off
setlocal

echo ============================================
echo   SolidWorksTools Update
echo ============================================
echo.

:: ── Pull latest changes ───────────────────────
echo [1/2] Pulling latest changes from GitHub...
git pull
if %errorlevel% neq 0 (
    echo [ERROR] git pull failed. Check your connection or repo access.
    pause
    exit /b 1
)

:: ── Update dependencies for each tool ─────────
echo.
echo [2/2] Updating dependencies...

for /d %%D in (*) do (
    if exist "%%D\.venv\Scripts\pip.exe" (
        echo   Updating %%D...
        "%%D\.venv\Scripts\pip.exe" install -r "%%D\requirements.txt" --quiet
    )
)

echo.
echo ============================================
echo   Update complete!
echo ============================================
echo.
pause
