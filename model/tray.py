"""
model/tray.py

Represents a single Logimat tray, combining data from:
 - LogimatLuExt
 - StockObjectBundle
"""

from utils.constants import DEFAULT_SPEED


class Tray:
    """Represents one tray within a Logimat."""

    def __init__(self, tray_no):
        self.trayNo = tray_no
        self.trayID = None
        self.trayHeight = None
        self.trayCycles = None

        # From StockObjectBundle
        self.originalRackSide = None
        self.originalSupportNo = None
        self.trayWidth = None
        self.trayLength = None
        self.maxLoad = None
        self.loadAidId = None

        # Defaults
        self.status = 256
        self.classABC = 0
        self.trayEmpty = False

        self.velocityHorizontal = DEFAULT_SPEED
        self.velocityVertical = DEFAULT_SPEED
        self.accelerationHorizontal = DEFAULT_SPEED
        self.accelerationVertical = DEFAULT_SPEED
        self.decelerationHorizontal = DEFAULT_SPEED
        self.decelerationVertical = DEFAULT_SPEED

    # ------------------------------------------------------------------
    def set_stock_data(self, rackside, supportno, tray_width, tray_length, tray_height, max_load, load_aid_id):
        """Set fields derived from StockObjectBundle."""
        self.originalRackSide = rackside
        self.originalSupportNo = supportno
        self.trayWidth = tray_width
        self.trayLength = tray_length
        self.trayHeight = tray_height
        self.maxLoad = max_load
        self.loadAidId = load_aid_id