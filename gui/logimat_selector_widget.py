# gui/logimat_selector_widget.py — SAFE VERSION

from PyQt6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QLabel
from db.queries import QUERY_LOAD_SCCCFG, table


class LogimatSelectorWidget(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db = db_manager

        layout = QVBoxLayout(self)

        self.label = QLabel("Select Logimat Units:", self)
        layout.addWidget(self.label)

        self.list_widget = QListWidget(self)
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.list_widget.setMaximumHeight(150)
        layout.addWidget(self.list_widget)

        # Load IDs immediately
        self.load_logimat_ids()

    def load_logimat_ids(self):
        try:
            rows = self.db.execute(
                QUERY_LOAD_SCCCFG.format(
                    table=table(self.db.schema, "SccCfgNgkp", self.db.db_type)
                )
            )
            self.list_widget.clear()
            for row in rows:
                logimat_id = row[0]
                self.list_widget.addItem(logimat_id)
        except Exception as exc:
            self.list_widget.clear()
            self.list_widget.addItem(f"Error: {exc}")

    def selected_ids(self):
        return [item.text() for item in self.list_widget.selectedItems()]