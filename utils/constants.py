"""
utils/constants.py

This module holds all static default values and hard-coded constants used
throughout the Logimat WEC JSON Generator. Keeping them here avoids duplication
and ensures consistency.

These values come directly from user‑specified rules.
"""

# ----------------------------
# MACHINE DEFAULT CONSTANTS
# ----------------------------
POSY_DEFAULT = -58.5

SUPPORT_DISTANCE = 125
OPENING_SUPPORT_DISTANCE = 50
OPENING_HEIGHT = 1000

SUPPORTS_FRONT = 1000
SUPPORTS_REAR = 1000

MAXIMUM_WEIGHT = 600
MAXIMUM_HEIGHT = 600

# Speeds
DEFAULT_SPEED = 100

# ----------------------------
# OPENING POSITIONING
# ----------------------------
OPENING_BASE_POSITION = 800
OPENING_INCREMENT = 2100  # Amount added for each stacked opening on same rackside

# ----------------------------
# MACHINE POSITION INCREMENT
# ----------------------------
LOGIMAT_FIRST_POSX = -5
LOGIMAT_POSX_INCREMENT = 3