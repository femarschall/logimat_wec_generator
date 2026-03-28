"""
db/oracle_connector.py

Optional Oracle support:
- First attempts cx_Oracle + Instant Client (full OCI mode)
- If unavailable, automatically falls back to python-oracledb (thin mode)
"""

# Try cx_Oracle first (full native mode)
try:
    import cx_Oracle
    ORACLE_AVAILABLE = True
    ORACLE_MODE = "cx_Oracle (OCI mode)"
    ORACLE_STATUS_MESSAGE = "Oracle support enabled using cx_Oracle."
except Exception:
    # Try thin-mode oracledb module
    try:
        import oracledb
        ORACLE_AVAILABLE = True
        ORACLE_MODE = "oracledb (thin mode)"
        ORACLE_STATUS_MESSAGE = (
            "Oracle connected in 'python-oracledb' Thin mode.\n"
            "Instant Client is not required, but some OCI features may be unavailable."
        )
    except Exception:
        ORACLE_AVAILABLE = False
        ORACLE_MODE = None
        ORACLE_STATUS_MESSAGE = (
            "Oracle support is disabled.\n"
            "Install either:\n"
            "  - cx_Oracle + Oracle Instant Client (recommended), OR\n"
            "  - python-oracledb (pure-Python thin mode)."
        )


class OracleConnector:
    """Oracle Database Connector supporting cx_Oracle and oracledb-thin."""

    def __init__(self, host, port, listener, username, password):
        if not ORACLE_AVAILABLE:
            raise RuntimeError(ORACLE_STATUS_MESSAGE)

        self.host = host
        self.port = port
        self.listener = listener
        self.username = username
        self.password = password
        self.conn = None

    def connect(self):
        """Create Oracle connection via whichever driver is available."""

        # Full OCI mode (Instant Client)
        if ORACLE_MODE.startswith("cx_Oracle"):
            try:
                dsn = cx_Oracle.makedsn(self.host, int(self.port), service_name=self.listener)
                self.conn = cx_Oracle.connect(self.username, self.password, dsn)
                return True
            except Exception as e:
                print("cx_Oracle connection error:", e)
                return False

        # Thin mode (pure Python)
        if ORACLE_MODE.startswith("oracledb"):
            try:
                dsn = f"{self.host}:{self.port}/{self.listener}"
                self.conn = oracledb.connect(user=self.username, password=self.password, dsn=dsn)
                return True
            except Exception as e:
                print("oracledb thin mode error:", e)
                return False

        return False

    def execute(self, sql, params=None):
        """Execute SQL query."""
        if not self.conn:
            return None

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params or {})
            return cursor.fetchall()
        except Exception as e:
            print("Oracle SQL error:", e)
            return None