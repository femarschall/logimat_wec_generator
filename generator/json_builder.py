"""
generator/json_builder.py

Converts LogimatMachine, Tray, and Opening model objects into the WEC JSON
structure used by the simulation core.

This module produces a Python dictionary matching the required JSON
format. The final dictionary is passed to wec_output.py for saving.
"""

import json


class WECJsonBuilder:
    """
    Build the WEC JSON output based on machine models.

    Output structure:

    {
        "com.ssn.simulation.core.Core": {
            "entities": [
                { "com.ssn.simulation.entities.Logimat": { ... } },
                { "com.ssn.simulation.entities.Logimat": { ... } },
                ...
            ],
            "gridSizeX": 0.0,
            "gridSizeY": 0.0,
            ...
        }
    }
    """

    def build_json(self, machines):
        """Build the full JSON structure from a list of LogimatMachine objects."""
        entities = []

        for m in machines:
            entity = self._build_logimat_entity(m)
            entities.append(entity)

        core = {
            "com.ssn.simulation.core.Core": {
                "entities": entities,
                "gridSizeX": 0.0,
                "gridSizeY": 0.0,
                "snapToGrid": True,
                "snapSizeX": 0.1,
                "snapSizeY": 0.1,
                "dockingDistance": 0.1,
                "resizeHandles": False,
                "connectionView": 0,
                "shadowView": 0,
                "detailsScale": 50.0,
                "connectionDetailsScale": 25.0,
                "showShadowConnections": False,
                "showDataTrackingConnections": False,
                "autoValidation": "HIGH",
                "showItemDetails": False,
                "showLastError": False,
                "repaintDirty": False,
                "reactionDelay": 25,
                "repaintDelay": 25,
                "randomColors": True,
                "wireFrame": False,
                "visuMode": False,
                "logLevel": 0,
                "logLongEventHandling": 0,
                "exitQuery": False,
                "saveRuntimeStateOnExit": False,
                "saveOpenRuntimeWindows": False,
                "backgroundColor": {"java.awt.Color": {"value": -1}},
                "gridColor": {"java.awt.Color": {"value": -4144960}},
                "connectionColor": {"java.awt.Color": {"value": -8355712}},
                "jumpConnectionColor": {"java.awt.Color": {"value": -10255680}},
                "headSelectionLineColor": {"java.awt.Color": {"value": -16777216}},
                "headSelectionFillColor": {"java.awt.Color": {"value": -3613198}},
                "tailSelectionLineColor": {"java.awt.Color": {"value": -16777216}},
                "tailSelectionFillColor": {"java.awt.Color": {"value": -10255680}},
                "fillSelectedEntities": False,
                "gridSelectionColor": {"java.awt.Color": {"value": -16777216}},
                "entityLineColor": {"java.awt.Color": {"value": -16777216}},
                "entityIdleColor": {"java.awt.Color": {"value": -1}},
                "entityErrorColor": {"java.awt.Color": {"value": -65536}},
                "entityBusyColor": {"java.awt.Color": {"value": -16744193}},
                "entityInterruptColor": {"java.awt.Color": {"value": -4144960}},
                "entityOccupiedColor1": {"java.awt.Color": {"value": -256}},
                "entityOccupiedColor2": {"java.awt.Color": {"value": -16711936}},
                "entityShadowColor": {"java.awt.Color": {"value": -4144960}},
                "itemLineColor": {"java.awt.Color": {"value": -16777216}},
                "itemFillColor": {"java.awt.Color": {"value": -4144960}},
                "sdxpReportingPointColor": {"java.awt.Color": {"value": -16744193}},
                "sdxpReportingPointScopeColor": {"java.awt.Color": {"value": -16725761}},
                "sdxpDirectionMarkColor": {"java.awt.Color": {"value": -26368}},
                "sdxpSegmentPointColor": {"java.awt.Color": {"value": -4727320}},
                "sdxpSegmentPointScopeColor": {"java.awt.Color": {"value": -4271386}},
                "sdxpPointOfInterestColor": {"java.awt.Color": {"value": -7155632}},
                "sdxpActionPointColor": {"java.awt.Color": {"value": -39169}},
                "buildNumber": 4001,
                "lastViewportX": -11.74,
                "lastViewportY": -2.17,
                "lastViewportScale": 70.0,
                "disableStatistics": False,
                "saveDomainsSeparately": False,
            }
        }

        return core

    # ----------------------------------------------------------------------
    # Build Logimat entity
    # ----------------------------------------------------------------------
    def _build_logimat_entity(self, machine):
        """
        Build JSON block for one Logimat machine.
        """
        trays = [self._build_tray_entity(t) for t in machine.trays]
        openings = [self._build_opening_entity(o) for o in machine.openings]

        logimat_json = {
            "com.ssn.simulation.entities.Logimat": {
                "id": machine.id,
                "posx": machine.posx,
                "posy": machine.posy,
                "sizex": 3.0,
                "sizey": 200.0,
                "sizez": 1.0,
                "transparent": False,
                "lastUpdate": 0,

                # Communication parameters
                "senderId": machine.senderId,
                "receiverId": machine.receiverId,
                "senderPort": machine.senderPort,
                "receiverPort": machine.receiverPort,

                # Machine-level properties
                "supportDistance": machine.supportDistance,
                "openingSupportDistance": machine.openingSupportDistance,
                "openingHeight": machine.openingHeight,
                "supportsFront": machine.supportsFront,
                "supportsRear": machine.supportsRear,
                "maximumHeight": machine.maximumHeight,
                "maximumWeight": machine.maximumWeight,

                # Movement parameters
                "horizontalSpeed": machine.horizontalSpeed,
                "verticalSpeed": machine.verticalSpeed,
                "horizontalAcceleration": machine.horizontalAcceleration,
                "verticalAcceleration": machine.verticalAcceleration,
                "horizontalDeceleration": machine.horizontalDeceleration,
                "verticalDeceleration": machine.verticalDeceleration,
                "globalSpeedSetting": machine.globalSpeedSetting,

                # PLC ID
                "plcId": machine.plcId,

                # Trays and openings
                "trays": trays,
                "openings": openings,
            }
        }

        return logimat_json

    # ----------------------------------------------------------------------
    def _build_tray_entity(self, tray):
        """Build JSON for one tray."""
        return {
            "com.ssn.simulation.entities.LogimatTray": {
                "trayNo": tray.trayNo,
                "status": tray.status,
                "maximumLoad": tray.maxLoad,
                "trayWeight": tray.maxLoad,    # weight = maxLoad for consistency
                "trayLoad": 0,
                "trayHeight": tray.trayHeight,
                "trayID": tray.trayID,
                "tilt": 0,
                "security": 0,
                "velocityHorizontal": tray.velocityHorizontal,
                "velocityVertical": tray.velocityVertical,
                "accelerationHorizontal": tray.accelerationHorizontal,
                "accelerationVertical": tray.accelerationVertical,
                "decelerationHorizontal": tray.decelerationHorizontal,
                "decelerationVertical": tray.decelerationVertical,
                "classABC": tray.classABC,
                "trayEmpty": tray.trayEmpty,
                "originalOpeningNo": 0,
                "originalRackSide": tray.originalRackSide,
                "originalSupportNo": tray.originalSupportNo,
                "floorHeight": 0,
                "floorType": 0,
                "trayCycles": tray.trayCycles,
            }
        }

    # ----------------------------------------------------------------------
    def _build_opening_entity(self, opening):
        """Build JSON for one opening."""
        return {
            "com.ssn.simulation.entities.LogimatOpening": {
                "side": opening.rackSide,
                "absolutePosition": opening.absolutePosition,
                "pointer": opening.pointer,
                "stubStatus": opening.stubStatus,
                "lightStatus": opening.lightStatus,
                "tiltStatus": opening.tiltStatus,
                "safeStatus": opening.safeStatus,
                "blockStatus": opening.blockStatus,
                "pointerX": opening.pointerX,
                "pointerZ": opening.pointerZ,
                "pointerHeight": opening.pointerHeight,
                "liftPosition": opening.liftPosition,
                "lightMode": opening.lightMode,
                "lightTimeout": opening.lightTimeout,
                "popup": opening.popup,
                "openingOperationMode": opening.openingOperationMode,
            }
        }