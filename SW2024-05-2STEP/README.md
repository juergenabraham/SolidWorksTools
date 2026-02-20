# SW2024-05-2STEP

Converts SolidWorks 2024 SP05 native files (`.sldprt`, `.sldasm`) to STEP format
using the SolidWorks COM API.

## Requirements

| Requirement | Version |
|---|---|
| Operating System | Windows |
| SolidWorks | 2024 SP05 |
| Python | >= 3.10 (dev/build only) |

## For End Users — Standalone Executable

No Python installation required.

1. Download `SW2024-05-2STEP.exe` from the releases page.
2. Double-click to launch the GUI.
3. Add one or more `.sldprt` / `.sldasm` files and click **Convert to STEP**.

## For Developers

### Setup

Run `setup.bat` once. It will:

- Install Python 3.11 automatically via `winget` if not already present.
- Create a virtual environment (`.venv`).
- Install all dependencies.

```bat
setup.bat
```

### Build Standalone Executable

After setup, run `build.bat` to produce `dist\SW2024-05-2STEP.exe`:

```bat
build.bat
```

### Create a Release

`release.bat` builds the `.exe`, tags the commit, and publishes a GitHub release
with the executable attached — all in one step.

Requirements:
- `setup.bat` has been run
- [GitHub CLI](https://cli.github.com) is installed and authenticated (`gh auth login`)

```bat
release.bat
```

You will be prompted for a version number (e.g. `1.0.0`).

### Run in Dev Mode

```bat
.venv\Scripts\activate

:: Launch GUI
python -m src --gui

:: Convert single file
python -m src path\to\file.sldprt
python -m src path\to\file.sldprt -o C:\output\result.step

:: Convert multiple files
python -m src file1.sldprt file2.sldasm file3.sldprt
python -m src file1.sldprt file2.sldasm -o C:\output\folder
```

## Dependencies

| Package | Purpose |
|---|---|
| `pywin32` | SolidWorks COM API access |
| `PyQt6` | Graphical user interface |
| `pyinstaller` | Standalone .exe build (dev only) |

## Project Structure

```
SW2024-05-2STEP/
  setup.bat             Developer setup (Python + venv + deps)
  build.bat             Build standalone .exe via PyInstaller
  sw2step.spec          PyInstaller build configuration
  pyproject.toml        Package metadata
  requirements.txt      Runtime dependencies
  requirements-dev.txt  Development dependencies (includes PyInstaller)
  README.md             This file
  doc.pdf               Generated documentation
  src/
    __init__.py
    __main__.py         Entry point (CLI + GUI launcher)
    converter.py        SolidWorks COM API conversion logic
    gui.py              PyQt6 graphical interface
```

## Notes

- SolidWorks must be **installed and licensed** on the machine.
- The converter attaches to a running SolidWorks instance if one is open,
  or starts a new one automatically.
- Supported input formats: `.sldprt` (part), `.sldasm` (assembly).
- Output is always a `.step` file (ISO 10303).
- The `dist/` and `build/` folders are excluded from version control.

## Version History

| Version | Date | Changes |
|---|---|---|
| 0.5.0 | 2026-02-20 | Batch conversion — multiple files via GUI list and CLI |
| 0.4.0 | 2026-02-20 | Run SolidWorks headless (no SW window during conversion) |
| 0.3.0 | 2026-02-20 | Add release.bat for one-step local GitHub release |
| 0.2.0 | 2026-02-20 | Add standalone .exe build via PyInstaller, replace install.py with setup.bat |
| 0.1.0 | 2026-02-20 | Initial release — CLI + GUI skeleton |
