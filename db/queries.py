"""
db/queries.py

Central location for SQL queries used by the application.

All table names must be prefixed with the provided schema name:
    SELECT * FROM <schema>.TableName
"""

# ---------------------------------------------------------
# Load Logimat IDs
# ---------------------------------------------------------

QUERY_LOGIMAT_IDS_FROM_LUEXT = """
SELECT DISTINCT luId
FROM {schema}.LogimatLuExt
WHERE luId IS NOT NULL
"""

QUERY_LOGIMAT_IDS_FROM_STOCK = """
SELECT DISTINCT
    LEFT(stoLoc_stoLocId, CHARINDEX('-', stoLoc_stoLocId) - 1) AS logimatId
FROM {schema}.StockObjectBundle
WHERE stoLoc_whLocId = 'LogiMat'
  AND stoLoc_stoLocId <> 'LogimatExt'
  AND CHARINDEX('-', stoLoc_stoLocId) > 0
  AND stoLoc_stoLocId NOT LIKE '%-%-%-%'   -- avoid multi-segment tray patterns
"""

QUERY_LOGIMAT_IDS_FROM_OPENING = """
SELECT DISTINCT logimatId
FROM {schema}.LogimatOpening
WHERE logimatId IS NOT NULL
"""

QUERY_LOGIMAT_IDS_FROM_SCCCFG = """
SELECT DISTINCT logimat_logimatId
FROM {schema}.SccCfgNgkp
WHERE logimat_logimatId IS NOT NULL
"""


# ---------------------------------------------------------
# Data extraction for full Logimat build
# ---------------------------------------------------------

QUERY_LOAD_TRAYS = """
SELECT
    luId,
    trayNo,
    trayBarcode,
    floorHeight,
    floorType,
    trayCycles
FROM {schema}.LogimatLuExt
WHERE luId = ?
"""

QUERY_LOAD_STOCK_FOR_LUID = """
SELECT
    stoLoc_stoLocId,
    loadAidId,
    grossDimension_x_value,
    grossDimension_y_value,
    grossDimension_z_value
FROM {schema}.StockObjectBundle
WHERE stoLoc_whLocId = 'LogiMat'
  AND stoLoc_stoLocId <> 'LogimatExt'
  AND stoLoc_stoLocId LIKE ? + '%'
"""

QUERY_LOAD_OPENINGS = """
SELECT
    openingNo,
    logimatId,
    rackSide
FROM {schema}.LogimatOpening
WHERE logimatId = ?
"""

QUERY_LOAD_SCCCFG = """
SELECT
    destAddrSoc,
    destAddrWamas,
    portSoc2Wamas,
    portWamas2Soc
FROM {schema}.SccCfgNgkp
WHERE logimat_logimatId = ?
"""