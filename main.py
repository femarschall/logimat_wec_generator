"""
main.py
Entry point for the Logimat WEC JSON Generator application.

This file initializes the PySide6 application, creates the main GUI window,
and launches the event loop.

Project Structure:
    main.py
    gui/
    db/
    model/
    generator/
    utils/
"""

import sys
import json
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon

from db.db_manager import DbManager
from gui.main_window import MainWindow


def load_settings():
    """Load persisted settings from settings.json with safe defaults."""
    default = {
        "hostname": "localhost",
        "port": "1433",
        "listener": "",
        "schema": "wls_prod",
        "username": "wls_prod",
        "password": "wls_prod",
        "db_type": "mssql",  # Default to MSSQL
    }

    try:
        with open("settings.json", "r", encoding="utf-8") as f:
            data = json.load(f)

            # Guarantee all expected fields exist
            for key, value in default.items():
                if key not in data:
                    data[key] = value

            return data

    except Exception:
        # First run OR corrupted file → return defaults
        return default


def save_settings(settings):
    """Save updated settings to settings.json."""
    with open("settings.json", "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)



def start_app():
    app = QApplication(sys.argv)

    # Load saved DB settings before GUI starts
    saved = load_settings()

    # Create empty DbManager (lazy connect)
    db = DbManager(
        hostname=saved["hostname"],
        port=saved["port"],
        listener=saved["listener"],
        schema=saved["schema"],
        username=saved["username"],
        password=saved["password"],
        db_type=saved["db_type"],
        auto_connect=False  # ← IMPORTANT
    )

    window = MainWindow(db, saved, save_settings)
    
    # Set application icon
    app.setWindowIcon(QIcon("gui/favicon.png"))
    
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    start_app()