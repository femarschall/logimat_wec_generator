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


# model/logimat_machine.py — FINAL FIXED VERSION

class LogimatMachine:
    def __init__(
        self,
        id,
        posx=0.0,
        posy=-58.5,
        plc_id=0,

        senderId=0,
        senderPort=0,
        receiverId=0,
        receiverPort=0,

        # fixed according to your rules
        supportsFront=1000,
        supportsRear=1000,

        openingSupportDistance=50,
        supportDistance=125,
        openingHeight=1000,

        maximumHeight=600,
        maximumWeight=600,

        horizontalSpeed=3.0,
        verticalSpeed=3.0,
        horizontalAcceleration=3.0,
        verticalAcceleration=3.0,
        horizontalDeceleration=5.0,
        verticalDeceleration=5.0,

        globalSpeedSetting=100
    ):
        self.id = id
        self.posx = posx
        self.posy = posy
        self.plcId = plc_id

        self.senderId = senderId
        self.senderPort = senderPort
        self.receiverId = receiverId
        self.receiverPort = receiverPort

        self.supportsFront = supportsFront
        self.supportsRear = supportsRear
        self.supportDistance = supportDistance
        self.openingSupportDistance = openingSupportDistance
        self.openingHeight = openingHeight

        self.maximumHeight = maximumHeight
        self.maximumWeight = maximumWeight

        self.horizontalSpeed = horizontalSpeed
        self.verticalSpeed = verticalSpeed
        self.horizontalAcceleration = horizontalAcceleration
        self.verticalAcceleration = verticalAcceleration
        self.horizontalDeceleration = horizontalDeceleration
        self.verticalDeceleration = verticalDeceleration

        self.globalSpeedSetting = globalSpeedSetting

        self.trays = []
        self.openings = []

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