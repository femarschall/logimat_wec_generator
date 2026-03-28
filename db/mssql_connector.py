# generator/db/mssql_connector.py — FINAL FIXED VERSION

import pyodbc

class MSSQLConnector:
    def __init__(self, hostname, port, listener, schema, username, password):
        self.hostname = hostname
        self.port = port
        self.listener = listener
        self.schema = schema
        self.username = username
        self.password = password
        self.conn = None

    def connect(self):
        # Build correct SERVER string
        if self.listener:   # named instance
            server = f"{self.hostname}\\{self.listener}"
        elif self.port:     # explicit port
            server = f"{self.hostname},{self.port}"
        else:               # default
            server = self.hostname

        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={server};"
            f"DATABASE={self.schema};"
            f"UID={self.username};"
            f"PWD={self.password};"
            "TrustServerCertificate=yes;"
        )

        self.conn = pyodbc.connect(connection_string, timeout=5)

    def execute(self, query, params=None):
        if not self.conn:
            raise RuntimeError("Database not connected.")

        cursor = self.conn.cursor()
        cursor.execute(query, params or [])
        rows = cursor.fetchall()
        cursor.close()
        return rows