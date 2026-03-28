# db/db_manager.py — FINAL, FIXED, CLEAN VERSION

class DbManager:
    def __init__(
        self,
        hostname="",
        port="",
        listener="",
        schema="",
        username="",
        password="",
        db_type="mssql",
        auto_connect=False,
    ):
        # Store connection parameters
        self.hostname = hostname
        self.port = port
        self.listener = listener
        self.schema = schema
        self.username = username
        self.password = password

        # Connector instance (MSSQL or Oracle)
        self.connector = None

        # Database type (mssql or oracle)
        self.db_type = db_type

        # DO NOT connect before QApplication
        if auto_connect:
            self.connect()

    # ---------------------------------------------------------
    # Lazy import for MSSQL connector (safe)
    # ---------------------------------------------------------
    def _load_mssql_connector(self):
        from db.mssql_connector import MSSQLConnector
        return MSSQLConnector

    # Lazy import for Oracle connector (safe)
    def _load_oracle_connector(self):
        from db.oracle_connector import OracleConnector
        return OracleConnector

    # ---------------------------------------------------------
    def connect(self):
        """
        Establish real DB connection.
        Takes NO parameters.
        Uses ONLY stored attributes.
        """

        if self.db_type == "mssql":
            MSSQLConnector = self._load_mssql_connector()
            self.connector = MSSQLConnector(
                hostname=self.hostname,
                port=self.port,
                listener=self.listener,
                schema=self.schema,
                username=self.username,
                password=self.password,
            )

        else:
            OracleConnector = self._load_oracle_connector()
            self.connector = OracleConnector(
                hostname=self.hostname,
                port=self.port,
                listener=self.listener,
                schema=self.schema,
                username=self.username,
                password=self.password,
            )

        # Make network connection
        self.connector.connect()

    # ---------------------------------------------------------
    def execute(self, query, params=None):
        if not self.connector:
            raise RuntimeError("Database not connected.")
        return self.connector.execute(query, params or [])

    # ---------------------------------------------------------
    def load_logimat_data(self, ids):
        from model.loader import LogimatDataLoader
        loader = LogimatDataLoader(self)
        return loader.load_logimat_data(ids)