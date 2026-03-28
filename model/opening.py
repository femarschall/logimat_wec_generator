"""
model/opening.py

Represents an opening for a Logimat machine.
The absolutePosition is computed based on:
 - rackSide (from DB)
 - stacked openings (increment logic defined by user).
"""

class Opening:
    """Represents a Logimat opening."""

    def __init__(self, opening_no, rack_side, absolute_position):
        self.openingNo = opening_no
        self.rackSide = rack_side
        self.absolutePosition = absolute_position

        # Defaults based on the example file
        self.pointer = False
        self.stubStatus = True
        self.lightStatus = False
        self.tiltStatus = False
        self.safeStatus = False
        self.blockStatus = False

        # Example values: these could be parameterized later if needed
        self.pointerX = 0
        self.pointerZ = 0
        self.pointerHeight = 0
        self.liftPosition = 0
        self.lightMode = 3
        self.lightTimeout = 0
        self.popup = False
        self.openingOperationMode = 1