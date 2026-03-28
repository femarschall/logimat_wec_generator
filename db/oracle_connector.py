# oracle_connector.py — FINAL FIXED VERSION (valid syntax)

ORACLE_AVAILABLE = False
ORACLE_MODE = None
ORACLE_STATUS_MESSAGE = "Oracle mode not yet checked."

def detect_oracle():
    """
    Run Oracle autodetection safely AFTER QApplication has started.
    """
    global ORACLE_AVAILABLE, ORACLE_MODE, ORACLE_STATUS_MESSAGE

    try:
        import cx_Oracle
        ORACLE_AVAILABLE = True
        ORACLE_MODE = "cx_Oracle"
        ORACLE_STATUS_MESSAGE = "Oracle support enabled using cx_Oracle."
        return cx_Oracle
    except Exception:
        pass

    try:
        import oracledb
        ORACLE_AVAILABLE = True
        ORACLE_MODE = "oracledb"
        ORACLE_STATUS_MESSAGE = (
            "Oracle connected using python-oracledb in thin mode."
        )
        return oracledb
    except Exception:
        pass

    ORACLE_AVAILABLE = False
    ORACLE_MODE = None
    ORACLE_STATUS_MESSAGE = (
        "Oracle support disabled. Install cx_Oracle or python-oracledb."
    )
    return None


class OracleConnector:
    def __init__(self, hostname, port, listener, schema, username, password):
        self.hostname = hostname
        self.port = port
        self.listener = listener
        self.schema = schema
        self.username = username
        self.password = password

        # Run detection only now (AFTER QApplication exists)
        self.driver = detect_oracle()

        if not ORACLE_AVAILABLE:
            raise RuntimeError("Oracle support is not available on this system.")

        self.conn = None

    def connect(self):
        """
        Creates a real Oracle connection (thin mode or cx_Oracle).
        """
        if ORACLE_MODE == "cx_Oracle":
            import cx_Oracle
            dsn = cx_Oracle.makedsn(self.hostname, self.port, service_name=self.listener)
            self.conn = cx_Oracle.connect(
                user=self.username,
                password=self.password,
                dsn=dsn,
                encoding="UTF-8"
            )
        else:
            import oracledb
            dsn = f"{self.hostname}:{self.port}/{self.listener}"
            self.conn = oracledb.connect(
                user=self.username,
                password=self.password,
                dsn=dsn
            )

    def execute(self, query, params=None):
        if not self.conn:
            raise RuntimeError("Oracle not connected.")

        cursor = self.conn.cursor()
        cursor.execute(query, params or [])
        rows = cursor.fetchall()
        cursor.close()
        return rows