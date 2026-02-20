@echo off
setlocal

echo ============================================
echo   SW2024-05-2STEP Setup
echo ============================================
echo.

:: ── 1. Check for Python ──────────────────────
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [1/3] Python not found. Installing via winget...
    winget install -e --id Python.Python.3.11 --silent
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Automatic Python installation failed.
        echo         Please install Python 3.11 manually from https://www.python.org
        echo         then re-run this script.
        pause
        exit /b 1
    )
    echo.
    echo [INFO] Python installed. Please close and re-open this window,
    echo        then run setup.bat again to complete the setup.
    pause
    exit /b 0
) else (
    echo [1/3] Python found:
    python --version
)

:: ── 2. Create virtual environment ────────────
echo.
if not exist ".venv" (
    echo [2/3] Creating virtual environment...
    python -m venv .venv
) else (
    echo [2/3] Virtual environment already exists — skipping.
)

:: ── 3. Install dependencies ───────────────────
echo.
echo [3/3] Installing dependencies...
.venv\Scripts\pip install --upgrade pip --quiet
.venv\Scripts\pip install -r requirements.txt

echo.
echo ============================================
echo   Setup complete!
echo ============================================
echo.
echo   To build the standalone .exe:
echo     build.bat
echo.
echo   To launch the GUI directly (dev mode):
echo     .venv\Scripts\activate
echo     python -m src --gui
echo.
pause
