# gui/main_window.py — FINAL FIXED VERSION (restored fields + safe imports)

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
)
from PyQt6.QtGui import QIcon
import os

from version import APP_VERSION
from gui.logimat_selector_widget import LogimatSelectorWidget
from gui.light_lines_selector_widget import LightLinesSelectorWidget
from generator.json_builder import WECJsonBuilder
from generator.wec_output import save_json_output


class MainWindow(QMainWindow):
    """
    Main screen with:
     - DB connection fields (hostname, port, listener, schema, user, password)
     - Test connection
     - Save settings
     - Logimat selector
     - JSON generator
     - Update checker
    """

    def __init__(self, db_manager, saved_settings, save_callback, parent=None):
        super().__init__(parent)

        self.db = db_manager
        self.saved_settings = saved_settings
        self.save_callback = save_callback

        self.setWindowTitle(f"Logimat WEC Generator v{APP_VERSION}")
        icon_path = os.path.join(os.path.dirname(__file__), "favicon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        central = QWidget(self)
        layout = QVBoxLayout(central)

        # ------------------------------------------------------------------
        # DATABASE SETTINGS PANEL (restored)
        # ------------------------------------------------------------------
        db_box = QVBoxLayout()

        row = QHBoxLayout()
        row.addWidget(QLabel("Database Type:"))
        self.cmb_db_type = QComboBox(self)
        self.cmb_db_type.addItem("MSSQL", "mssql")
        self.cmb_db_type.addItem("Oracle", "oracle")
        # Set current selection based on saved settings
        current_db_type = self.saved_settings.get("db_type", "mssql")
        if current_db_type == "oracle":
            self.cmb_db_type.setCurrentIndex(1)
        else:
            self.cmb_db_type.setCurrentIndex(0)
        row.addWidget(self.cmb_db_type)
        db_box.addLayout(row)

        layout.addLayout(db_box)

        row = QHBoxLayout()
        row.addWidget(QLabel("Hostname:"))
        self.txt_host = QLineEdit(self.saved_settings["hostname"])
        self.txt_host.setPlaceholderText("localhost or IP address")
        row.addWidget(self.txt_host)
        db_box.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel("Port:"))
        self.txt_port = QLineEdit(self.saved_settings["port"])
        self.txt_port.setPlaceholderText("Defaults: MSSQL=1433 / Oracle=1521")
        row.addWidget(self.txt_port)
        db_box.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel("Listener / Service:"))
        self.txt_listener = QLineEdit(self.saved_settings["listener"])
        row.addWidget(self.txt_listener)
        db_box.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel("Schema / DB Name:"))
        self.txt_schema = QLineEdit(self.saved_settings["schema"])
        self.txt_schema.setPlaceholderText("wls_prod")
        row.addWidget(self.txt_schema)
        db_box.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel("Username:"))
        self.txt_user = QLineEdit(self.saved_settings["username"])
        self.txt_user.setPlaceholderText("wls_prod")
        self.txt_user.setPlaceholderText("wls_prod")        
        row.addWidget(self.txt_user)
        db_box.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel("Password:"))
        self.txt_password = QLineEdit(self.saved_settings["password"])
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_password.setPlaceholderText("wls_prod")
        row.addWidget(self.txt_password)
        db_box.addLayout(row)

        # Buttons row
        btn_row = QHBoxLayout()

        # TEST CONNECTION button
        self.btn_test = QPushButton("Test Connection")
        self.btn_test.clicked.connect(self.test_connection)
        btn_row.addWidget(self.btn_test)

        # CONNECT button
        self.btn_connect = QPushButton("Connect")
        self.btn_connect.clicked.connect(self.connect_now)
        btn_row.addWidget(self.btn_connect)
        
        # SAVE SETTINGS button
        self.btn_save = QPushButton("Save Settings")
        self.btn_save.clicked.connect(self.save_settings)
        btn_row.addWidget(self.btn_save)

        layout.addLayout(btn_row)

        # ------------------------------------------------------------------
        # LOGIMAT SELECTOR
        # ------------------------------------------------------------------
        self.selector = LogimatSelectorWidget(self.db, self)
        layout.addWidget(self.selector)

        # ------------------------------------------------------------------
        # PUT 2 LIGHT SELECTOR
        # ------------------------------------------------------------------
        self.light_lines_selector = LightLinesSelectorWidget(self.db, self)
        layout.addWidget(self.light_lines_selector)

        # ------------------------------------------------------------------
        # ACTION BUTTONS
        # ------------------------------------------------------------------
        self.btn_generate = QPushButton("Generate JSON")
        self.btn_generate.clicked.connect(self.generate_json)
        layout.addWidget(self.btn_generate)

        self.btn_check_update = QPushButton("Check for Updates")
        self.btn_check_update.clicked.connect(self.check_update)
        layout.addWidget(self.btn_check_update)

        # ------------------------------------------------------------------
        self.setCentralWidget(central)
        self.statusBar().showMessage(f"Logimat WEC Generator v{APP_VERSION}")

    # ----------------------------------------------------------------------
    def connect_now(self):
        """Perform an actual DB connection and keep it open for the session."""
        # Update db_type from UI selection
        self.db.db_type = self.cmb_db_type.currentData()
        
        self.db.hostname = self.txt_host.text()
        self.db.port = self.txt_port.text()
        self.db.listener = self.txt_listener.text()
        self.db.schema = self.txt_schema.text()
        self.db.username = self.txt_user.text()
        self.db.password = self.txt_password.text()

        try:
            self.db.connect()
            QMessageBox.information(self, "Connected", "Database connection established.")
            
            # ⭐ RELOAD LOGIMAT LIST AFTER CONNECTING
            self.selector.load_logimat_ids()
            self.light_lines_selector.load_light_lines()

        except Exception as exc:
            QMessageBox.critical(self, "Connection Failed", str(exc))
    # ----------------------------------------------------------------------
    def test_connection(self):
        """Apply DB fields and test connection."""
        # Update db_type from UI selection
        self.db.db_type = self.cmb_db_type.currentData()
        
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

    # ----------------------------------------------------------------------
    def save_settings(self):
        """Persist DB settings to settings.json."""
        settings = {
            "hostname": self.txt_host.text(),
            "port": self.txt_port.text(),
            "listener": self.txt_listener.text(),
            "schema": self.txt_schema.text(),
            "username": self.txt_user.text(),
            "password": self.txt_password.text(),
            "db_type": self.cmb_db_type.currentData(),
        }

        self.save_callback(settings)
        QMessageBox.information(self, "Saved", "Settings saved.")

    # ----------------------------------------------------------------------
    def generate_json(self):
        ids = self.selector.selected_ids()
        if not ids:
            QMessageBox.warning(self, "No selection", "Select at least one Logimat ID.")
            return

        try:
            machines = self.db.load_logimat_data(ids)
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))
            return

        # Get selected Put 2 Light gadgets
        light_line_gadgets = None
        if self.light_lines_selector.is_enabled():
            light_line_gadgets = self.light_lines_selector.get_selected_gadgets()

        builder = WECJsonBuilder()
        json_text = builder.build_json(machines, light_line_gadgets)
        save_json_output(self, json_text)

    # ----------------------------------------------------------------------
    def check_update(self):
        from gui.settings_window import check_update_dialog
        check_update_dialog(self)