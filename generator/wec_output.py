"""
generator/wec_output.py

Handles saving the generated WEC JSON structure to a user‑selected file.
Provides a file‑dialog interface (via PySide6) to choose the location.
"""


from PyQt6.QtWidgets import QFileDialog, QMessageBox

def save_json_output(parent, json_text):
    """
    Save JSON output to a file.
    """
    path, _ = QFileDialog.getSaveFileName(
        parent,
        "Save JSON",
        "",
        "JSON Files (*.json)"
    )

    if not path:
        return

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(json_text)

        QMessageBox.information(parent, "Saved", "JSON saved successfully.")
    except Exception as exc:
        QMessageBox.critical(parent, "Error", str(exc))