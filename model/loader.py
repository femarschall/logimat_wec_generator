"""
model/loader.py

This module is responsible for loading all Logimat-related data from
the database and constructing model objects for:

 - LogimatMachine
 - Tray
 - Opening

It enforces **all** business rules defined by the user, including:
 - Parsing stoLocId
 - loadAidId weight extraction
 - tray dimensions
 - opening position computation
 - posx increments
 - sequential PLC IDs
"""

from utils.parser import (
    parse_sto_location,
    extract_max_load_from_loadAidId,
)
from utils.constants import (
    LOGIMAT_FIRST_POSX,
    LOGIMAT_POSX_INCREMENT,
    OPENING_BASE_POSITION,
    OPENING_INCREMENT,
)
from model.logimat_machine import LogimatMachine
from model.tray import Tray
from model.opening import Opening

from db.queries import (
    QUERY_LOAD_TRAYS,
    QUERY_LOAD_STOCK_FOR_LUID,
    QUERY_LOAD_OPENINGS,
    QUERY_LOAD_SCCCFG
)


class LogimatDataLoader:
    """Loads and assembles full Logimat machines from the DB."""

    def __init__(self, db_manager):
        self.db = db_manager

    # ------------------------------------------------------------------
    def load_logimat_data(self, selected_ids):
        """
        Build LogimatMachine objects for each selected Logimat ID.

        Returns:
            list[LogimatMachine]
        """
        machines = []
        posx = LOGIMAT_FIRST_POSX
        plc_counter = 1

        for lid in selected_ids:
            machine = LogimatMachine(lid, posx, plc_counter)

            # Load communication parameters
            self._load_comm(machine)

            # Load trays
            self._load_trays(machine)

            # Load openings
            self._load_openings(machine)

            machines.append(machine)

            posx += LOGIMAT_POSX_INCREMENT
            plc_counter += 1

        return machines

    # ------------------------------------------------------------------
    def _load_comm(self, machine):
        """Load senderId/receiverId/ports from SccCfgNgkp."""
        rows = self.db.execute(QUERY_LOAD_SCCCFG.format(schema=self.db.schema), [machine.id])
        if rows:
            row = rows[0]
            machine.set_comm_parameters(
                sender_id=row[0],
                receiver_id=row[1],
                port_s2w=row[2],
                port_w2s=row[3],
            )

    # ------------------------------------------------------------------
    def _load_trays(self, machine):
        """Load trays from LogimatLuExt and enrich with StockObjectBundle data."""
        rows = self.db.execute(QUERY_LOAD_TRAYS.format(schema=self.db.schema), [machine.id])
        if not rows:
            return

        for (luId, trayNo, trayBarcode, floorHeight, floorType, trayCycles) in rows:
            tray = Tray(trayNo)
            tray.trayID = trayBarcode
            tray.trayCycles = trayCycles

            # Load matching stock objects using stoLoc prefix (logimatId)
            stock_rows = self.db.execute(
                QUERY_LOAD_STOCK_FOR_LUID.format(schema=self.db.schema),
                [machine.id]
            )

            if stock_rows:
                # We attempt to match trays logically based on stoLoc_stoLocId grouping
                for (stoLocId, loadAidId, dim_x, dim_y, dim_z) in stock_rows:
                    parsed = parse_sto_location(stoLocId)

                    if parsed is None:
                        continue

                    logimat_id, rack_side, support_no = parsed

                    if logimat_id != machine.id:
                        continue

                    max_load = extract_max_load_from_loadAidId(loadAidId)

                    tray.set_stock_data(
                        rackside=rack_side,
                        supportno=support_no,
                        tray_width=dim_x,
                        tray_length=dim_y,
                        tray_height=dim_z,
                        max_load=max_load,
                        load_aid_id=loadAidId,
                    )

            machine.add_tray(tray)

    # ------------------------------------------------------------------
    def _load_openings(self, machine):
        """Load openings and compute absolute positions."""
        rows = self.db.execute(
            QUERY_LOAD_OPENINGS.format(schema=self.db.schema),
            [machine.id]
        )
        if not rows:
            return

        # Sort based on your rule: order by openingNo, then rackSide
        rows_sorted = sorted(rows, key=lambda r: (r[0], r[2]))

        # Group openings by rackSide to compute stacked positions
        rackside_counter = {}

        for (openingNo, logimatId, rackSide) in rows_sorted:
            count = rackside_counter.get(rackSide, 0)

            abs_pos = OPENING_BASE_POSITION + (count * OPENING_INCREMENT)
            rackside_counter[rackSide] = count + 1

            opening = Opening(opening_no=openingNo, rack_side=rackSide, absolute_position=abs_pos)
            machine.add_opening(opening)