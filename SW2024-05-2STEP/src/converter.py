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
    """Attach to a running SolidWorks instance, or start a new one."""
    try:
        app = win32com.client.GetActiveObject("SldWorks.Application")
        print("[INFO] Connected to existing SolidWorks instance.")
    except Exception:
        print("[INFO] Starting new SolidWorks instance...")
        app = win32com.client.Dispatch("SldWorks.Application")
        app.Visible = True
    return app


def convert_to_step(input_path: str, output_path: str | None = None) -> str:
    """
    Convert a SolidWorks file to STEP format.

    Parameters
    ----------
    input_path  : Path to the .sldprt or .sldasm file.
    output_path : Optional path for the output .step file.
                  Defaults to same directory as input with .step extension.

    Returns
    -------
    Absolute path of the generated STEP file.

    Raises
    ------
    ValueError   : Unsupported file extension.
    RuntimeError : SolidWorks could not open or export the file.
    """
    input_path = Path(input_path).resolve()
    ext = input_path.suffix.lower()

    if ext not in DOC_TYPES:
        raise ValueError(
            f"Unsupported file type '{ext}'. Supported: {list(DOC_TYPES.keys())}"
        )

    output_path = (
        Path(output_path).resolve()
        if output_path
        else input_path.with_suffix(".step")
    )

    swApp = connect_solidworks()
    doc_type = DOC_TYPES[ext]

    errors   = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    warnings = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)

    swDoc = swApp.OpenDoc6(str(input_path), doc_type, 1, "", errors, warnings)

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

    print(f"[OK] Exported: {output_path}")
    return str(output_path)
