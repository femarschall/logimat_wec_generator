"""
model/logimat_machine.py

Defines the LogimatMachine class, which aggregates:
 - Machine‑level configuration (senderId, receiverId, ports)
 - All trays for this machine
 - All openings for this machine

This model acts as the central in‑memory representation of each Logimat.
"""

from utils.constants import (
    SUPPORT_DISTANCE,
    OPENING_SUPPORT_DISTANCE,
    OPENING_HEIGHT,
    SUPPORTS_FRONT,
    SUPPORTS_REAR,
    MAXIMUM_HEIGHT,
    MAXIMUM_WEIGHT,
    DEFAULT_SPEED,
    POSY_DEFAULT,
)


class LogimatMachine:
    """Represents one complete Logimat machine."""

    def __init__(self, logimat_id, posx, plc_id):
        self.id = logimat_id
        self.posx = posx
        self.posy = POSY_DEFAULT

        # Communication parameters (filled after reading SccCfgNgkp)
        self.senderId = None
        self.receiverId = None
        self.senderPort = None
        self.receiverPort = None

        # Default machine characteristics
        self.supportDistance = SUPPORT_DISTANCE
        self.openingSupportDistance = OPENING_SUPPORT_DISTANCE
        self.openingHeight = OPENING_HEIGHT
        self.supportsFront = SUPPORTS_FRONT
        self.supportsRear = SUPPORTS_REAR
        self.maximumHeight = MAXIMUM_HEIGHT
        self.maximumWeight = MAXIMUM_WEIGHT

        # Movement speeds
        self.horizontalSpeed = DEFAULT_SPEED
        self.verticalSpeed = DEFAULT_SPEED
        self.horizontalAcceleration = DEFAULT_SPEED
        self.verticalAcceleration = DEFAULT_SPEED
        self.horizontalDeceleration = DEFAULT_SPEED
        self.verticalDeceleration = DEFAULT_SPEED
        self.globalSpeedSetting = DEFAULT_SPEED

        # PLC ID (sequential)
        self.plcId = plc_id

        # Logimat contents
        self.trays = []      # list of Tray instances
        self.openings = []   # list of Opening instances

    # ----------------------------------------------------------------------
    def add_tray(self, tray):
        """Append a tray to this machine."""
        self.trays.append(tray)

    def add_opening(self, opening):
        """Append an opening to this machine."""
        self.openings.append(opening)

    # ----------------------------------------------------------------------
    def set_comm_parameters(self, sender_id, receiver_id, port_s2w, port_w2s):
        """Set communication IDs and ports."""
        self.senderId = sender_id
        self.receiverId = receiver_id
        self.senderPort = port_s2w
        self.receiverPort = port_w2s