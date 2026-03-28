"""
gui/logimat_selector_widget.py

Provides the checkbox interface to let the user select which Logimats
will be included in the generated WEC JSON output.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox


class LogimatSelectorWidget(QWidget):
    """
    Displays a checkbox list of Logimat IDs.
    """

    def __init__(self, logimat_ids):
        super().__init__()

        layout = QVBoxLayout(self)

        self.checkboxes = []

        for lid in sorted(logimat_ids):
            cb = QCheckBox(lid)
            layout.addWidget(cb)
            self.checkboxes.append(cb)

        layout.addStretch()

    def get_selected_ids(self):
        """Return a list of selected Logimat IDs."""
        return [cb.text() for cb in self.checkboxes if cb.isChecked()]