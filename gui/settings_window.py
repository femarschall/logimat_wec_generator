# --- Update Checker Dialog (used by main_window) ---------------------------

import requests
from version import APP_VERSION, UPDATE_URL
from PyQt6.QtWidgets import QMessageBox

def check_update_dialog(parent):
    """
    Pops a simple modal dialog showing whether an update is available.
    """
    try:
        response = requests.get(UPDATE_URL, timeout=3)
        latest = response.text.strip()

        if latest != APP_VERSION:
            QMessageBox.information(
                parent,
                "Update Available",
                f"A new version ({latest}) is available.\n"
                f"Current version: {APP_VERSION}"
            )
        else:
            QMessageBox.information(
                parent,
                "Up to Date",
                f"You are running the latest version ({APP_VERSION})."
            )
    except Exception as exc:
        QMessageBox.warning(
            parent,
            "Update Check Failed",
            f"Could not check for updates:\n{exc}"
        )

def test_connection(self):
    self.db.hostname = self.txt_host.text()
    self.db.port = self.txt_port.text()
    self.db.listener = self.txt_listener.text()
    self.db.schema = self.txt_schema.text()
    self.db.username = self.txt_user.text()
    self.db.password = self.txt_password.text()

    try:
        self.db.connect()
        QMessageBox.information(self, "OK", "Connection successful!")
    except Exception as exc:
        QMessageBox.critical(self, "Error", str(exc))