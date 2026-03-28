"""
gui/main_window.py

This module contains the main PySide6 GUI window for the
Logimat WEC JSON Generator.

Responsibilities:
 - Collect DB configuration (engine, host, schema, ports)
 - Connect to the selected database
 - Load Logimat IDs from DB
 - Display checkbox list for selecting which Logimats to include
 - Trigger the JSON generator
 - Provide user feedback (status bar, messages)

This is the central user-facing component.
"""

from db.oracle_connector import ORACLE_AVAILABLE, ORACLE_STATUS_MESSAGE

from PySide6.QtWidgets import (
    QWidget, QMainWindow, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox, QScrollArea,
    QGroupBox, QFormLayout
)
from PySide6.QtCore import Qt

from db.db_manager import DBManager
from gui.logimat_selector_widget import LogimatSelectorWidget
from model.loader import LogimatDataLoader
from generator.json_builder import WECJsonBuilder
from generator.wec_output import save_json_output


class MainWindow(QMainWindow):
    """
    Main GUI window of the application.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Logimat WEC JSON Generator")
        self.setMinimumSize(900, 700)

        # Database manager instance
        self.db_manager = DBManager()

        # UI Components
        self.engine_combo = QComboBox()
        self.txt_host = QLineEdit()
        self.txt_port = QLineEdit()
        self.txt_listener = QLineEdit()
        self.txt_schema = QLineEdit()
        self.txt_user = QLineEdit()
        self.txt_password = QLineEdit()

        self.selector_widget = None  # Created after DB connect
        self.btn_generate = QPushButton("Generate JSON")
        self.btn_connect = QPushButton("Connect to Database")
        self.btn_test = QPushButton("Test Connection")

        self._build_ui()
        self.btn_generate.setEnabled(False)

    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    def _build_ui(self):
        """Construct the application layout."""
        central = QWidget()
        main_layout = QVBoxLayout(central)

        # =============================
        # Database Config Form
        # =============================
        form_box = QGroupBox("Database Configuration")
        form_layout = QFormLayout()
        
        self.engine_combo.addItem("MSSQL")
        if ORACLE_AVAILABLE:
            self.engine_combo.addItem("ORACLE")
        else:
            # Optional: show message so user knows why Oracle is missing
            QMessageBox.information(
                self,
                "Oracle Support Disabled",
                ORACLE_STATUS_MESSAGE
            )
            
        form_layout.addRow("Database Engine:", self.engine_combo)

        self.txt_host.setPlaceholderText("Hostname or IP")
        form_layout.addRow("Host:", self.txt_host)

        self.txt_listener.setPlaceholderText("Oracle Listener / Service Name (Oracle only)")
        form_layout.addRow("Oracle Listener:", self.txt_listener)

        self.txt_port.setPlaceholderText("1433 for MSSQL, 1521 for Oracle")
        form_layout.addRow("Port:", self.txt_port)

        self.txt_schema.setPlaceholderText("WAMAS Schema (e.g. WAMASPRD)")
        form_layout.addRow("WAMAS Schema:", self.txt_schema)

        self.txt_user.setPlaceholderText("Database Username")
        form_layout.addRow("Username:", self.txt_user)

        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setPlaceholderText("Database Password")
        form_layout.addRow("Password:", self.txt_password)

        form_box.setLayout(form_layout)
        main_layout.addWidget(form_box)

        # =============================
        # Buttons
        # =============================
        btn_row = QHBoxLayout()
        btn_row.addWidget(self.btn_connect)
        btn_row.addWidget(self.btn_generate)
        btn_row.addWidget(self.btn_test)


        self.btn_connect.clicked.connect(self.on_connect_clicked)
        self.btn_generate.clicked.connect(self.on_generate_clicked)
        self.btn_test.clicked.connect(self.on_test_connection)

        main_layout.addLayout(btn_row)

        # =============================
        # Scroll area for Logimat selector
        # =============================
        scroll_box = QGroupBox("Select Logimat Units")
        scroll_layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        scroll_layout.addWidget(self.scroll_area)
        scroll_box.setLayout(scroll_layout)

        main_layout.addWidget(scroll_box)

        self.setCentralWidget(central)
        
        
        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        main_layout.addWidget(self.log_console)
        
        def log(self, message):
            self.log_console.append(message)


    # ------------------------------------------------------------------
    # Database Connect
    # ------------------------------------------------------------------
    def on_connect_clicked(self):
        """Triggered when user clicks 'Connect to Database'."""
        engine = self.engine_combo.currentText()
        host = self.txt_host.text().strip()
        port = self.txt_port.text().strip()
        listener = self.txt_listener.text().strip()
        schema = self.txt_schema.text().strip()
        user = self.txt_user.text().strip()
        password = self.txt_password.text().strip()

        # Input validation
        if not host or not port or not schema or not user or not password:
            QMessageBox.warning(self, "Missing Values", "Please fill in all fields.")
            return

        ok = self.db_manager.connect(
            engine=engine,
            host=host,
            port=port,
            listener=listener,
            schema=schema,
            username=user,
            password=password,
        )

        if not ok:
            QMessageBox.critical(self, "Connection Failed", "Could not connect to database.")
            return

        # Load Logimat IDs from DB
        logimat_ids = self.db_manager.load_logimat_ids()

        if not logimat_ids:
            QMessageBox.warning(self, "No Logimat IDs", "No Logimat units found in DB.")
            return

        # Create Logimat selector widget
        self.selector_widget = LogimatSelectorWidget(logimat_ids)
        self.scroll_area.setWidget(self.selector_widget)

        self.btn_generate.setEnabled(True)
        QMessageBox.information(self, "Connected", "Successfully connected to DB!")

    # ------------------------------------------------------------------
    # Generate JSON
    # ------------------------------------------------------------------
    def on_generate_clicked(self):
        """Triggered when user clicks 'Generate JSON'."""
        if not self.selector_widget:
            QMessageBox.warning(self, "No Data", "Please connect to DB first.")
            return

        selected = self.selector_widget.get_selected_ids()

        if not selected:
            QMessageBox.warning(self, "Nothing Selected", "Please select at least one Logimat.")
            return

        loader = LogimatDataLoader(self.db_manager)
        machines = loader.load_logimat_data(selected)

        builder = WECJsonBuilder()
        json_data = builder.build_json(machines)

        save_json_output(self, json_data)
        QMessageBox.information(self, "Success", "WEC JSON file generated successfully!")
        
    # ------------------------------------------------------------------
    # Test Connection
    # ------------------------------------------------------------------
    def on_test_connection(self):
        engine = self.engine_combo.currentText()
        host = self.txt_host.text().strip()
        port = self.txt_port.text().strip()
        listener = self.txt_listener.text().strip()
        schema = self.txt_schema.text().strip()
        user = self.txt_user.text().strip()
        password = self.txt_password.text().strip()

        ok = self.db_manager.connect(engine, host, port, listener, schema, user, password)

        if ok:
            self.log("Connection test successful.")
            QMessageBox.information(self, "Success", "Connection successful!")
        else:
            self.log("Connection test FAILED.")
            QMessageBox.critical(self, "Error", "Connection failed.")