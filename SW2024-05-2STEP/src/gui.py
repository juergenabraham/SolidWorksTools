"""
PyQt6 GUI for SW2024-05-2STEP.
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel,
    QFileDialog, QTextEdit,
)
from PyQt6.QtCore import QThread, pyqtSignal


class ConversionWorker(QThread):
    """Runs the conversion in a background thread to keep the UI responsive."""

    finished = pyqtSignal(str)
    error    = pyqtSignal(str)

    def __init__(self, input_path: str, output_path: str | None):
        super().__init__()
        self.input_path  = input_path
        self.output_path = output_path

    def run(self):
        try:
            from converter import convert_to_step
            result = convert_to_step(self.input_path, self.output_path)
            self.finished.emit(result)
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

        # --- Input file ---
        layout.addWidget(QLabel("SolidWorks File (.sldprt / .sldasm):"))
        input_row = QHBoxLayout()
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("Select input file…")
        btn_in = QPushButton("Browse…")
        btn_in.clicked.connect(self._browse_input)
        input_row.addWidget(self.input_edit)
        input_row.addWidget(btn_in)
        layout.addLayout(input_row)

        # --- Output file ---
        layout.addWidget(QLabel("Output STEP File (optional — defaults to same folder):"))
        output_row = QHBoxLayout()
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("Select output file…")
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
    def _browse_input(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select SolidWorks File", "",
            "SolidWorks Files (*.sldprt *.sldasm);;All Files (*)",
        )
        if path:
            self.input_edit.setText(path)

    def _browse_output(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save STEP File", "",
            "STEP Files (*.step *.stp);;All Files (*)",
        )
        if path:
            self.output_edit.setText(path)

    def _convert(self):
        input_path = self.input_edit.text().strip()
        if not input_path:
            self._log_error("No input file selected.")
            return

        output_path = self.output_edit.text().strip() or None

        self.convert_btn.setEnabled(False)
        self.statusBar().showMessage("Converting…")
        self._log(f"Converting: {input_path}")

        self._worker = ConversionWorker(input_path, output_path)
        self._worker.finished.connect(self._on_success)
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _on_success(self, output_path: str):
        self._log(f"[OK] Exported to: {output_path}")
        self.statusBar().showMessage("Done.")
        self.convert_btn.setEnabled(True)

    def _on_error(self, msg: str):
        self._log_error(msg)
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
