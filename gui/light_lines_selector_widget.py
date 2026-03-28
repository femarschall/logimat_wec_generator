# gui/light_lines_selector_widget.py

from PyQt6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QLabel, QCheckBox
from db.queries import QUERY_LOAD_DCLC_GADGETS, table


class LightLinesSelectorWidget(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db = db_manager

        layout = QVBoxLayout(self)

        # Checkbox to enable/disable Put 2 Light
        self.checkbox = QCheckBox("Include Put 2 Light (PBL Gadgets)", self)
        self.checkbox.setChecked(False)
        layout.addWidget(self.checkbox)

        self.label = QLabel("Select Put 2 Light:", self)
        layout.addWidget(self.label)

        self.list_widget = QListWidget(self)
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.list_widget.setMaximumHeight(70)
        layout.addWidget(self.list_widget)

        # Load Put 2 Light data
        self.load_light_lines()

    def load_light_lines(self):
        try:
            rows = self.db.execute(
                QUERY_LOAD_DCLC_GADGETS.format(
                    table=table(self.db.schema, "DcLcGadget", self.db.db_type)
                )
            )
            self.list_widget.clear()

            # Group by station, cfg, and line for consolidated display
            seen_lines = set()
            for row in rows:
                station_id = row[10]  # station_stationId
                cfg_id = row[2]       # line_cfg_cfgId
                line_id = row[1]      # line_lineId

                line_key = f"{station_id} - {cfg_id} - Line {line_id}"
                if line_key not in seen_lines:
                    seen_lines.add(line_key)
                    self.list_widget.addItem(line_key)

        except Exception as exc:
            self.list_widget.clear()
            self.list_widget.addItem(f"Error: {exc}")

    def is_enabled(self):
        return self.checkbox.isChecked()

    def selected_lines(self):
        """Return list of selected line identifiers in format 'station-cfg-line'"""
        if not self.is_enabled():
            return []

        selected_items = [item.text() for item in self.list_widget.selectedItems()]
        # Parse back to components
        lines = []
        for item in selected_items:
            # Format: "station - cfg - Line line_id"
            parts = item.split(" - ")
            if len(parts) >= 3:
                station = parts[0].strip()
                cfg = parts[1].strip()
                line_part = parts[2].strip()
                if line_part.startswith("Line "):
                    line_id = line_part[5:].strip()
                    lines.append((station, cfg, line_id))
        return lines

    def get_selected_gadgets(self):
        """Return all gadgets for selected lines"""
        if not self.is_enabled():
            return []

        selected_lines = self.selected_lines()
        if not selected_lines:
            return []

        try:
            all_gadgets = self.db.execute(
                QUERY_LOAD_DCLC_GADGETS.format(
                    table=table(self.db.schema, "DcLcGadget", self.db.db_type)
                )
            )

            selected_gadgets = []
            for gadget in all_gadgets:
                station_id = gadget[10]  # station_stationId
                cfg_id = gadget[2]       # line_cfg_cfgId
                line_id = str(gadget[1]) # line_lineId

                # Check if this gadget's line is selected
                for sel_station, sel_cfg, sel_line in selected_lines:
                    if station_id == sel_station and cfg_id == sel_cfg and line_id == sel_line:
                        selected_gadgets.append(gadget)
                        break

            return selected_gadgets

        except Exception as exc:
            print(f"Error loading gadgets: {exc}")
            return []