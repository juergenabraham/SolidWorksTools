"""
SolidWorks COM API — core conversion logic.
Requires SolidWorks 2024 SP05 and pywin32 to be installed.
"""

import pythoncom
import win32com.client
from pathlib import Path

# SolidWorks document type constants
DOC_TYPES = {
    ".sldprt": 1,  # swDocPART
    ".sldasm": 2,  # swDocASSEMBLY
    ".slddrw": 3,  # swDocDRAWING
}


def connect_solidworks():
    """Attach to a running SolidWorks instance, or start a new headless one."""
    try:
        app = win32com.client.GetActiveObject("SldWorks.Application")
        print("[INFO] Connected to existing SolidWorks instance.")
    except Exception:
        print("[INFO] Starting SolidWorks in background...")
        app = win32com.client.Dispatch("SldWorks.Application")
        app.Visible = False       # no SW window
        app.UserControl = False   # automation mode — SW exits when we're done
    return app


def _convert_single(swApp, input_path: Path, output_path: Path) -> str:
    """Convert one file using an existing SolidWorks connection."""
    ext = input_path.suffix.lower()
    if ext not in DOC_TYPES:
        raise ValueError(
            f"Unsupported file type '{ext}'. Supported: {list(DOC_TYPES.keys())}"
        )

    errors   = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    warnings = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)

    swDoc = swApp.OpenDoc6(str(input_path), DOC_TYPES[ext], 1, "", errors, warnings)
    if swDoc is None:
        raise RuntimeError(
            f"SolidWorks could not open '{input_path}' "
            f"(errors={errors.value}, warnings={warnings.value})"
        )

    ret = swDoc.SaveAs3(str(output_path), 0, 0)
    swApp.CloseDoc(str(input_path))

    if not output_path.exists():
        raise RuntimeError(
            f"Export failed — SaveAs3 returned {ret}. "
            "Check that SolidWorks has STEP export enabled."
        )

    return str(output_path)


def convert_to_step(input_path: str, output_path: str | None = None) -> str:
    """
    Convert a single SolidWorks file to STEP format.

    Parameters
    ----------
    input_path  : Path to the .sldprt or .sldasm file.
    output_path : Optional path for the output .step file.
                  Defaults to same directory as input with .step extension.

    Returns
    -------
    Absolute path of the generated STEP file.
    """
    input_path  = Path(input_path).resolve()
    output_path = (
        Path(output_path).resolve() if output_path
        else input_path.with_suffix(".step")
    )

    swApp  = connect_solidworks()
    result = _convert_single(swApp, input_path, output_path)
    print(f"[OK] Exported: {result}")
    return result


def convert_batch(
    input_paths: list[str],
    output_dir: str | None = None,
    progress_callback=None,
) -> tuple[list[str], list[tuple[str, str]]]:
    """
    Convert multiple SolidWorks files in a single SolidWorks session.

    Parameters
    ----------
    input_paths       : List of paths to .sldprt or .sldasm files.
    output_dir        : Optional output directory.
                        Defaults to each file's own directory.
    progress_callback : Optional callable(current, total, path) for UI updates.

    Returns
    -------
    (successes, failures)
    successes : list of output STEP file paths
    failures  : list of (input_path, error_message)
    """
    swApp     = connect_solidworks()
    successes = []
    failures  = []
    total     = len(input_paths)

    for i, raw_path in enumerate(input_paths, 1):
        input_path = Path(raw_path).resolve()

        output_path = (
            Path(output_dir) / input_path.with_suffix(".step").name
            if output_dir
            else input_path.with_suffix(".step")
        )

        if progress_callback:
            progress_callback(i, total, str(input_path))

        try:
            result = _convert_single(swApp, input_path, output_path)
            successes.append(result)
            print(f"[OK] ({i}/{total}) {result}")
        except Exception as exc:
            failures.append((str(input_path), str(exc)))
            print(f"[ERROR] ({i}/{total}) {input_path}: {exc}")

    return successes, failures
