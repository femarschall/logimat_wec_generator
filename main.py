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
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    """Start the GUI application."""
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()