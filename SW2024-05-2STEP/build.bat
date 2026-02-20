@echo off
setlocal

echo ============================================
echo   Building SW2024-05-2STEP.exe
echo ============================================
echo.

:: ── Check venv ────────────────────────────────
if not exist ".venv" (
    echo [ERROR] Virtual environment not found.
    echo         Please run setup.bat first.
    pause
    exit /b 1
)

:: ── Install PyInstaller ───────────────────────
echo [1/2] Installing build dependencies...
.venv\Scripts\pip install pyinstaller>=6.0 --quiet

:: ── Build ─────────────────────────────────────
echo.
echo [2/2] Building executable...
.venv\Scripts\pyinstaller sw2step.spec --clean

:: ── Report ────────────────────────────────────
echo.
if exist "dist\SW2024-05-2STEP.exe" (
    echo ============================================
    echo   Build successful!
    echo   Output: dist\SW2024-05-2STEP.exe
    echo ============================================
) else (
    echo [ERROR] Build failed. See output above for details.
    exit /b 1
)
echo.
pause
