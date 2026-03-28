"""
db/db_manager.py

This module is responsible for:
 - Managing the connection to either MSSQL or Oracle.
 - Providing a unified interface for running queries.
 - Loading Logimat IDs from the database (based on multiple tables).
 - Passing through the correct connector based on engine selection.

This acts as the main database abstraction layer for the application.
"""

from db.oracle_connector import OracleConnector
from db.mssql_connector import MSSQLConnector
from db.queries import (
    QUERY_LOGIMAT_IDS_FROM_LUEXT,
    QUERY_LOGIMAT_IDS_FROM_STOCK,
    QUERY_LOGIMAT_IDS_FROM_OPENING,
    QUERY_LOGIMAT_IDS_FROM_SCCCFG
)

class DBManager:
    """Central DB manager supporting Oracle and MSSQL."""

    def __init__(self):
        self.engine = None
        self.connector = None
        self.schema = None

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------
    def connect(self, engine, host, port, listener, schema, username, password):
        self.engine = engine.upper()
        self.schema = schema
            
        if self.engine == "ORACLE":
            from db.oracle_connector import OracleConnector, ORACLE_AVAILABLE

            if not ORACLE_AVAILABLE:
                print("Oracle support disabled — cx_Oracle not available.")
                return False

            self.connector = OracleConnector(host, port, listener, username, password)
        else:
            from db.mssql_connector import MSSQLConnector
            # automatically append .dbo to schema
            self.schema = f"{schema}.dbo"
            
            self.connector = MSSQLConnector(host, port, username, password, schema)

        return self.connector.connect()

    # ------------------------------------------------------------------
    # Execute query
    # ------------------------------------------------------------------
    def execute(self, sql, params=None):
        """Run a SQL query using the active connector."""
        if not self.connector:
            return None

        return self.connector.execute(sql, params)

    # ------------------------------------------------------------------
    # Load distinct Logimat IDs
    # ------------------------------------------------------------------
    def load_logimat_ids(self):
        """
        Aggregate Logimat IDs across multiple tables:
         - LogimatLuExt
         - StockObjectBundle
         - LogimatOpening
         - SccCfgNgkp

        Return: sorted list of unique IDs.
        """

        ids = set()

        # From LogimatLuExt
        rows = self.execute(QUERY_LOGIMAT_IDS_FROM_LUEXT.format(schema=self.schema))
        if rows:
            for r in rows:
                if r[0]:
                    ids.add(r[0])

        # From StockObjectBundle stoLoc
        rows = self.execute(QUERY_LOGIMAT_IDS_FROM_STOCK.format(schema=self.schema))
        if rows:
            for r in rows:
                if r[0]:
                    ids.add(r[0])

        # From LogimatOpening
        rows = self.execute(QUERY_LOGIMAT_IDS_FROM_OPENING.format(schema=self.schema))
        if rows:
            for r in rows:
                if r[0]:
                    ids.add(r[0])

        # From SccCfgNgkp
        rows = self.execute(QUERY_LOGIMAT_IDS_FROM_SCCCFG.format(schema=self.schema))
        if rows:
            for r in rows:
                if r[0]:
                    ids.add(r[0])

        return sorted(ids)