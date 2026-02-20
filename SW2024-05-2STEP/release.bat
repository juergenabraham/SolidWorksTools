@echo off
setlocal

echo ============================================
echo   SW2024-05-2STEP Release
echo ============================================
echo.

:: ── Check prerequisites ───────────────────────
if not exist ".venv" (
    echo [ERROR] Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)

gh --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] GitHub CLI ^(gh^) not found.
    echo         Install from https://cli.github.com
    pause
    exit /b 1
)

:: ── Get version ───────────────────────────────
set /p VERSION=Enter version number (e.g. 1.0.0):
if "%VERSION%"=="" (
    echo [ERROR] No version entered.
    pause
    exit /b 1
)

set TAG=v%VERSION%
set EXE=dist\SW2024-05-2STEP.exe

echo.
echo Building and releasing %TAG%...

:: ── Build ─────────────────────────────────────
echo.
echo [1/3] Building executable...
.venv\Scripts\pip install "pyinstaller>=6.0" --quiet
.venv\Scripts\pyinstaller sw2step.spec --clean

if not exist "%EXE%" (
    echo [ERROR] Build failed. See output above.
    pause
    exit /b 1
)

:: ── Tag ───────────────────────────────────────
echo.
echo [2/3] Creating git tag %TAG%...
git tag %TAG%
if %errorlevel% neq 0 (
    echo [ERROR] Tag %TAG% already exists or git failed.
    pause
    exit /b 1
)
git push origin %TAG%

:: ── GitHub Release ────────────────────────────
echo.
echo [3/3] Creating GitHub release %TAG%...
gh release create %TAG% "%EXE%" ^
    --title "SW2024-05-2STEP %TAG%" ^
    --generate-notes

if %errorlevel% neq 0 (
    echo [ERROR] GitHub release creation failed. See output above.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Release %TAG% published successfully!
echo ============================================
echo.
pause
