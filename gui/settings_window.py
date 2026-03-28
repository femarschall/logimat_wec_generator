import json
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DB Presets")

        self.file = "settings.json"

        layout = QVBoxLayout()
        form = QFormLayout()

        self.txt_host = QLineEdit()
        self.txt_port = QLineEdit()
        self.txt_schema = QLineEdit()
        self.txt_user = QLineEdit()

        form.addRow("Host:", self.txt_host)
        form.addRow("Port:", self.txt_port)
        form.addRow("Schema:", self.txt_schema)
        form.addRow("Username:", self.txt_user)

        layout.addLayout(form)

        btn_save = QPushButton("Save Preset")
        btn_save.clicked.connect(self.save)
        layout.addWidget(btn_save)

        self.setLayout(layout)
        self.load()

    def load(self):
        try:
            with open(self.file) as f:
                data = json.load(f)
            self.txt_host.setText(data.get("host", ""))
            self.txt_port.setText(data.get("port", ""))
            self.txt_schema.setText(data.get("schema", ""))
            self.txt_user.setText(data.get("user", ""))
        except:
            pass

    def save(self):
        data = {
            "host": self.txt_host.text(),
            "port": self.txt_port.text(),
            "schema": self.txt_schema.text(),
            "user": self.txt_user.text(),
        }
        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)
        self.accept()