# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for SW2024-05-2STEP
# Build with: pyinstaller sw2step.spec --clean

block_cipher = None

a = Analysis(
    ['src/__main__.py'],
    pathex=['.', 'src'],
    binaries=[],
    datas=[],
    hiddenimports=[
        # pywin32 / SolidWorks COM API
        'win32com',
        'win32com.client',
        'win32com.server',
        'pythoncom',
        'pywintypes',
        # PyQt6
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SW2024-05-2STEP',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,       # windowed app — no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,           # set to 'icon.ico' if you add an icon later
)
