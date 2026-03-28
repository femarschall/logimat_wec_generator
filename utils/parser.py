"""
utils/parser.py

Contains helper parsing functions:
 - stoLoc parsing (extracting logimatId, rackSide, supportNo)
 - loadAidId parsing (maxLoad extracted before "T")
 - safe conversions and string utilities
"""

import re


def parse_sto_location(sto_loc_id: str):
    """
    Parse a stoLoc_stoLocId into components.

    Expected format:
        "<logimatId>-<rackSide>-<supportNo>"

    Example:
        "A1-1-001" → ("A1", 1, 1)

    Returns:
        (logimatId, rackSide, supportNo)
    """
    if sto_loc_id == "LogimatExt":
        return None

    try:
        logimat_id, rack_side_str, support_str = sto_loc_id.split("-")
        return logimat_id, int(rack_side_str), int(support_str)
    except Exception:
        return None


def extract_max_load_from_loadAidId(load_aid_id: str):
    """
    Extract the max load from the prefix of loadAidId until the letter 'T'.

    Example:
        "310T3025x815" → 310
        "630T3025x815" → 630
    """
    if not load_aid_id:
        return None

    match = re.match(r"(\d+)T", load_aid_id)
    if match:
        return int(match.group(1))

    return None


def safe_int(value, default=0):
    """Convert to integer safely."""
    try:
        return int(value)
    except Exception:
        return default


def safe_float(value, default=0.0):
    """Convert to float safely."""
    try:
        return float(value)
    except Exception:
        return default