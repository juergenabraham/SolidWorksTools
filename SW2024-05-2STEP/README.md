# SW2024-05-2STEP

Converts SolidWorks 2024 SP05 native files (`.sldprt`, `.sldasm`) to STEP format
using the SolidWorks COM API.

## Requirements

| Requirement | Version |
|---|---|
| Operating System | Windows |
| SolidWorks | 2024 SP05 |
| Python | >= 3.10 |

## Dependencies

| Package | Purpose |
|---|---|
| `pywin32` | SolidWorks COM API access |
| `PyQt6` | Graphical user interface |

## Setup

Run the installer once to create a virtual environment and install all dependencies:

```bat
python install.py
```

Then activate the environment:

```bat
.venv\Scripts\activate
```

## Usage

### GUI

```bat
python -m src --gui
```

Or simply run without arguments:

```bat
python -m src
```

### CLI

```bat
python -m src path\to\file.sldprt
python -m src path\to\file.sldasm -o C:\output\result.step
```

## Project Structure

```
SW2024-05-2STEP/
  install.py        Setup script (creates venv + installs deps)
  pyproject.toml    Package metadata
  requirements.txt  Python dependencies
  README.md         This file
  doc.pdf           Generated documentation
  src/
    __init__.py
    __main__.py     Entry point (CLI + GUI launcher)
    converter.py    SolidWorks COM API conversion logic
    gui.py          PyQt6 graphical interface
```

## Notes

- SolidWorks must be **installed and licensed** on the machine.
- The converter will attach to a running SolidWorks instance if one is open,
  or start a new one automatically.
- Supported input formats: `.sldprt` (part), `.sldasm` (assembly).
- Output is always a `.step` file (ISO 10303).

## Version History

| Version | Date | Changes |
|---|---|---|
| 0.1.0 | 2026-02-20 | Initial release — CLI + GUI skeleton |
