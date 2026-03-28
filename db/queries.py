# ---------------------------------------------------------------
# Table helper — must be at very top, not inside any docstring
# ---------------------------------------------------------------

def table(schema, table_name, db_type):
    """
    Oracle  → schema.table
    MSSQL   → schema.dbo.table
    """
    if db_type.lower() == "oracle":
        return f"{schema}.{table_name}"
    else:
        return f"{schema}.dbo.{table_name}"


# ---------------------------------------------------------------
# QUERIES BELOW — using dynamic table() helper
# ---------------------------------------------------------------

QUERY_LOAD_SCCCFG = """
SELECT
    id,
    whLocId,
    hostname,
    portWamas2Soc,
    portSoc2Wamas,
    destAddrSoc,
    destAddrWamas
FROM {table}
"""


QUERY_LOAD_TRAYS = """
SELECT 
    luId,
    trayNo,
    trayBarcode,
    floorHeight,
    floorType,
    trayCycles
FROM {table}
WHERE logimat_logimatId = ?
"""


QUERY_LOAD_STOCK_BY_LUID = """
SELECT
    luId,
    stoLoc_stoLocId,
    loadAidId,
    grossDimension_x_value,
    grossDimension_y_value,
    grossDimension_z_value,
    keyData_grossWeight_value
FROM {table}
WHERE luId = ?
  AND stoLoc_whLocId = 'LogiMat'
  AND stoLoc_stoLocId <> 'LogimatExt'
"""


QUERY_LOAD_OPENINGS = """
SELECT
    openingNo,
    logimatId,
    rackSide
FROM {table}
WHERE logimatId = ?
"""


QUERY_LOAD_DCLC_GADGETS = """
SELECT
    gadgetId,
    line_lineId,
    line_cfg_cfgId,
    line_cfg_whLocId,
    pickSequence,
    type,
    gadgetError,
    gadgetState,
    location_stoLocId,
    location_whLocId,
    station_stationId,
    station_whLocId
FROM {table}
ORDER BY line_lineId, gadgetId
"""