"""
generator/wec_output.py

Handles saving the generated WEC JSON structure to a user‑selected file.
Provides a file‑dialog interface (via PySide6) to choose the location.
"""

import json
from PySide6.QtWidgets import QFileDialog, QMessageBox


def save_json_output(parent, json_data):
    """
    Save the JSON structure to disk using a Save File dialog.
    """
    filename, _ = QFileDialog.getSaveFileName(
        parent,
        "Save WEC JSON File",
        "logimat_wec.json",
        "JSON Files (*.json)"
    )

    if not filename:
        return

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)
    except Exception as e:
        QMessageBox.critical(parent, "Save Error", f"Failed to save file:\n{e}")