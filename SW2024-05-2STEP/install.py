"""
Setup script — creates a virtual environment and installs all dependencies.
Run with: python install.py
"""

import subprocess
import sys
from pathlib import Path


def run(cmd: list, **kwargs):
    print(f"  > {' '.join(str(c) for c in cmd)}")
    subprocess.run(cmd, check=True, **kwargs)


def main():
    print("=" * 45)
    print("  SW2024-05-2STEP Setup")
    print("=" * 45)

    venv = Path(".venv")

    # Step 1: virtual environment
    if not venv.exists():
        print("\n[1/3] Creating virtual environment...")
        run([sys.executable, "-m", "venv", str(venv)])
    else:
        print("\n[1/3] Virtual environment already exists — skipping.")

    pip = venv / "Scripts" / "pip.exe"

    # Step 2: upgrade pip
    print("\n[2/3] Upgrading pip...")
    run([str(pip), "install", "--upgrade", "pip"])

    # Step 3: install dependencies
    print("\n[3/3] Installing dependencies...")
    run([str(pip), "install", "-r", "requirements.txt"])

    print("\n" + "=" * 45)
    print("  Setup complete!")
    print("=" * 45)
    print("\nActivate the environment:")
    print("  .venv\\Scripts\\activate")
    print("\nLaunch the GUI:")
    print("  python -m src --gui")
    print("\nConvert a file via CLI:")
    print("  python -m src path\\to\\file.sldprt")
    print("  python -m src path\\to\\file.sldprt -o output.step")


if __name__ == "__main__":
    main()
