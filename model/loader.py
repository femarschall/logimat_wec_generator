# loader.py — FINAL FIXED VERSION (matching your existing SELECT sequences)

from model.tray import Tray
from model.opening import Opening
from db.queries import (
    QUERY_LOAD_SCCCFG,
    QUERY_LOAD_TRAYS,
    QUERY_LOAD_STOCK_BY_LUID,
    QUERY_LOAD_OPENINGS,
    table
)


class LogimatDataLoader:
    def __init__(self, db_manager):
        self.db = db_manager

    # -----------------------------------------------------------
    def load_logimat_data(self, ids):
        machines = []

        # Load all config rows
        cfg_rows = self.db.execute(
            QUERY_LOAD_SCCCFG.format(
                table=table(self.db.schema, "SccCfgNgkp", self.db.db_type)
            )
        )

        # FIX: Correct map: id → row
        cfg_map = { row[0]: row for row in cfg_rows }

        for index, logimat_id in enumerate(ids):
            machine = self._load_machine_structure(logimat_id, index, cfg_map)
            self._load_trays(machine)
            self._load_openings(machine)
            machines.append(machine)

        return machines

    # -----------------------------------------------------------
    def _load_machine_structure(self, logimat_id, index, cfg_map):
        from model.logimat_machine import LogimatMachine

        posx = -5 + (index * 3)
        posy = -58.5
        plc_id = index + 1

        # Defaults
        senderPort   = 0
        receiverPort = 0
        senderId     = plc_id
        receiverId   = plc_id

        if logimat_id in cfg_map:
            cfg = cfg_map[logimat_id]

            # Indexes based on YOUR SELECT statement:
            # 0 id
            # 1 whLocId
            # 2 hostname
            # 3 portWamas2Soc
            # 4 portSoc2Wamas
            # 5 destAddrSoc
            # 6 destAddrWamas

            senderPort   = int(cfg[3])
            receiverPort = int(cfg[4])
            senderId     = int(cfg[5])
            receiverId   = int(cfg[6])

        machine = LogimatMachine(
            id=logimat_id,
            posx=posx,
            posy=posy,
            plc_id=plc_id,
            senderId=senderId,
            senderPort=senderPort,
            receiverId=receiverId,
            receiverPort=receiverPort
        )

        return machine

    # -----------------------------------------------------------
    def _load_trays(self, machine):
        query = QUERY_LOAD_TRAYS.format(
            table=table(self.db.schema, "LogimatLuExt", self.db.db_type)
        )
        
        print("TRAY QUERY:", query)
        print("PARAM:", machine.id)
        rows = self.db.execute(query, [machine.id])
        print("TRAY ROWS:", rows)


        for (luId, trayNo, trayBarcode, floorHeight, floorType, trayCycles) in rows:

            tray = Tray(int(trayNo))
            tray.trayID = trayBarcode
            tray.trayCycles = int(trayCycles)

            # Load stock
            stock_query = QUERY_LOAD_STOCK_BY_LUID.format(
                table=table(self.db.schema, "StockObjectBundle", self.db.db_type)
            )
            stock_rows = self.db.execute(stock_query, [luId])

            if not stock_rows:
                continue

            (
                _,
                stoLoc,
                loadAidId,
                dim_x,
                dim_y,
                dim_z,
                gross_weight
            ) = stock_rows[0]

            if stoLoc == "LogimatExt":
                continue

            try:
                _, rackSideStr, supportStr = stoLoc.split("-")
                tray.originalRackSide = int(rackSideStr)
                tray.originalSupportNo = int(supportStr)
            except:
                continue

            tray.trayWidth = int(dim_x)
            tray.trayLength = int(dim_y)
            tray.trayHeight = int(dim_z)

            try:
                tray.maxLoad = int(loadAidId)
            except:
                tray.maxLoad = 0

            tray.trayEmpty = (gross_weight == 0)

            machine.add_tray(tray)

    # -----------------------------------------------------------
    def _load_openings(self, machine):
        query = QUERY_LOAD_OPENINGS.format(
            table=table(self.db.schema, "LogimatOpening", self.db.db_type)
        )
        print("OPEN QUERY:", query)
        print("PARAM:", machine.id)
        rows = self.db.execute(query, [machine.id])
        print("OPEN ROWS:", rows)

        for (openingNo, logimatId, rackSide) in rows:
            opening = Opening(
                opening_no=int(openingNo),
                rack_side=int(rackSide),
                absolute_position=0
            )
            machine.add_opening(opening)