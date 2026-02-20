"""
Entry point — supports both CLI and GUI usage.

CLI:  python -m src path\\to\\file.sldprt [-o output.step]
GUI:  python -m src --gui
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
        "input", nargs="?",
        help="Input SolidWorks file (.sldprt or .sldasm)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output STEP file path (default: same folder as input)",
    )
    parser.add_argument(
        "--gui", action="store_true",
        help="Launch the graphical user interface",
    )

    args = parser.parse_args()

    if args.gui or args.input is None:
        from gui import launch_gui
        launch_gui()
    else:
        from converter import convert_to_step
        try:
            output = convert_to_step(args.input, args.output)
            print(f"Success: {output}")
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
