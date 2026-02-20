"""
PyQt6 GUI for SW2024-05-2STEP.
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel,
    QFileDialog, QTextEdit, QListWidget,
    QAbstractItemView,
)
from PyQt6.QtCore import QThread, pyqtSignal


class ConversionWorker(QThread):
    """Runs batch conversion in a background thread to keep the UI responsive."""

    progress = pyqtSignal(int, int, str)   # current, total, path
    finished = pyqtSignal(list, list)      # successes, failures
    error    = pyqtSignal(str)

    def __init__(self, input_paths: list[str], output_dir: str | None):
        super().__init__()
        self.input_paths = input_paths
        self.output_dir  = output_dir or None

    def run(self):
        try:
            from converter import convert_batch
            successes, failures = convert_batch(
                self.input_paths,
                self.output_dir,
                progress_callback=lambda cur, tot, path: self.progress.emit(cur, tot, path),
            )
            self.finished.emit(successes, failures)
        except Exception as exc:
            self.error.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SW2024-05-2STEP — SolidWorks to STEP Converter")
        self.setMinimumWidth(640)
        self._worker = None
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # --- File list ---
        layout.addWidget(QLabel("SolidWorks Files (.sldprt / .sldasm):"))

        btn_row = QHBoxLayout()
        btn_add    = QPushButton("Add Files...")
        btn_remove = QPushButton("Remove Selected")
        btn_clear  = QPushButton("Clear")
        btn_add.clicked.connect(self._add_files)
        btn_remove.clicked.connect(self._remove_selected)
        btn_clear.clicked.connect(self._clear_files)
        btn_row.addWidget(btn_add)
        btn_row.addWidget(btn_remove)
        btn_row.addWidget(btn_clear)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.file_list.setFixedHeight(140)
        layout.addWidget(self.file_list)

        # --- Output folder ---
        layout.addWidget(QLabel("Output Folder (optional — defaults to each file's folder):"))
        output_row = QHBoxLayout()
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("Select output folder…")
        btn_out = QPushButton("Browse…")
        btn_out.clicked.connect(self._browse_output)
        output_row.addWidget(self.output_edit)
        output_row.addWidget(btn_out)
        layout.addLayout(output_row)

        # --- Convert button ---
        self.convert_btn = QPushButton("Convert to STEP")
        self.convert_btn.setFixedHeight(36)
        self.convert_btn.clicked.connect(self._convert)
        layout.addWidget(self.convert_btn)

        # --- Log ---
        layout.addWidget(QLabel("Log:"))
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(160)
        layout.addWidget(self.log)

        self.statusBar().showMessage("Ready")

    # ------------------------------------------------------------------
    def _add_files(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Select SolidWorks Files", "",
            "SolidWorks Files (*.sldprt *.sldasm);;All Files (*)",
        )
        for path in paths:
            # avoid duplicates
            existing = [self.file_list.item(i).text()
                        for i in range(self.file_list.count())]
            if path not in existing:
                self.file_list.addItem(path)
        self._update_status()

    def _remove_selected(self):
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))
        self._update_status()

    def _clear_files(self):
        self.file_list.clear()
        self._update_status()

    def _browse_output(self):
        path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if path:
            self.output_edit.setText(path)

    def _update_status(self):
        count = self.file_list.count()
        self.statusBar().showMessage(f"{count} file(s) queued." if count else "Ready")

    # ------------------------------------------------------------------
    def _convert(self):
        input_paths = [
            self.file_list.item(i).text()
            for i in range(self.file_list.count())
        ]
        if not input_paths:
            self._log_error("No files selected.")
            return

        output_dir = self.output_edit.text().strip() or None

        self.convert_btn.setEnabled(False)
        self.statusBar().showMessage(f"Converting 0/{len(input_paths)}…")
        self._log(f"Starting batch conversion of {len(input_paths)} file(s).")

        self._worker = ConversionWorker(input_paths, output_dir)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._on_finished)
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _on_progress(self, current: int, total: int, path: str):
        self._log(f"({current}/{total}) Converting: {path}")
        self.statusBar().showMessage(f"Converting {current}/{total}…")

    def _on_finished(self, successes: list, failures: list):
        self._log(f"Done. {len(successes)} succeeded, {len(failures)} failed.")
        for path, err in failures:
            self._log_error(f"{path}: {err}")
        self.statusBar().showMessage(
            f"Done — {len(successes)} succeeded, {len(failures)} failed."
        )
        self.convert_btn.setEnabled(True)

    def _on_error(self, msg: str):
        self._log_error(f"Unexpected error: {msg}")
        self.statusBar().showMessage("Error.")
        self.convert_btn.setEnabled(True)

    def _log(self, msg: str):
        self.log.append(f"[INFO] {msg}")

    def _log_error(self, msg: str):
        self.log.append(f"[ERROR] {msg}")


def launch_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
