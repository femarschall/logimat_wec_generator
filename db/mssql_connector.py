"""
db/mssql_connector.py

Handles Microsoft SQL Server connections using pyodbc.
"""

import pyodbc


class MSSQLConnector:
    """MSSQL Database Connector."""

    def __init__(self, host, port, username, password, schema):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.schema = schema
        self.conn = None

    def connect(self):
        """Establish connection to MSSQL using pyodbc."""
        try:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.host},{self.port};"
                f"UID={self.username};"
                f"PWD={self.password};"
            )
            self.conn = pyodbc.connect(conn_str)
            return True
        except Exception as e:
            print("MSSQL connection error:", e)
            return False

    def execute(self, sql, params=None):
        """Execute SQL query and return all rows."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print("MSSQL SQL error:", e)
            return None