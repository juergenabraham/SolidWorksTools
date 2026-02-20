"""
Entry point — supports both CLI and GUI usage.

CLI (single file):
  python -m src file.sldprt [-o output.step]

CLI (multiple files):
  python -m src file1.sldprt file2.sldasm [-o C:\\output\\folder]

GUI:
  python -m src --gui
  python -m src          (no arguments also opens the GUI)
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="sw2step",
        description="SW2024-05-2STEP — Convert SolidWorks 2024 SP05 files to STEP format",
    )
    parser.add_argument(
        "input", nargs="*",
        help="One or more SolidWorks files (.sldprt or .sldasm)",
    )
    parser.add_argument(
        "-o", "--output",
        help=(
            "Single file: output STEP path. "
            "Multiple files: output folder (defaults to each file's own folder)."
        ),
    )
    parser.add_argument(
        "--gui", action="store_true",
        help="Launch the graphical user interface",
    )

    args = parser.parse_args()

    if args.gui or not args.input:
        from gui import launch_gui
        launch_gui()

    elif len(args.input) == 1:
        from converter import convert_to_step
        try:
            output = convert_to_step(args.input[0], args.output)
            print(f"Success: {output}")
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

    else:
        from converter import convert_batch
        successes, failures = convert_batch(args.input, output_dir=args.output)
        if failures:
            for path, err in failures:
                print(f"[FAILED] {path}: {err}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
