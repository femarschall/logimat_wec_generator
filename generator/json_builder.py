"""
json_builder.py — Final WEC-Compliant Builder
This version is fully aligned with the WEC example file provided by the user
(logimat_pbl.json) and with the structure found in the user's current builder.
"""

import json


class WECJsonBuilder:
    """
    Produces JSON matching the WEC simulator structure:

    {
        "com.ssn.simulation.core.Core": {
            "entities": [
                { "com.ssn.simulation.entities.Logimat": {...} },
                ...
            ],
            <core settings>
        }
    }
    """

    # ------------------------------------------------------------------
    def build_json(self, machines, light_line_gadgets=None):
        """
        Build final WEC JSON from a list of LogimatMachine instances.
        Optionally include light line gadgets.
        """
        entities = []

        # Append one Logimat entity per machine
        for m in machines:
            entities.append(self._build_logimat(m))

        # Add additional entities after logimats
        entities.extend([
            {
                "com.ssn.simulation.entities.ConnectorNGKP": {
                    "id": "ConnectorNGKP1",
                    "posx": -5.9,
                    "posy": 6.8,
                    "sizex": 1.0,
                    "sizey": 1.0,
                    "sizez": 1.0,
                    "transparent": False,
                    "lastUpdate": 0,
                    "autoConnect": True,
                    "clientMode": False,
                    "acknowledgeTimeout": 10000,
                    "aliveTelegramRate": 30000,
                    "disconnectIdleTime": 90000,
                    "autoConfigure": True,
                    "shuttlePortRange": "50001-59999"
                }
            },
            {
                "com.ssn.simulation.entities.ConnectorPCX": {
                    "id": "ConnectorPCX3",
                    "posx": -4.4,
                    "posy": 6.8,
                    "sizex": 1.0,
                    "sizey": 1.0,
                    "sizez": 1.0,
                    "transparent": False,
                    "lastUpdate": 1560250028699,
                    "autoConnect": True,
                    "connections": [
                        {
                            "com.ssn.simulation.entities.ConnectorPCXConnection": {
                                "name": "1",
                                "commandPort": 9200,
                                "statusPort": 8787
                            }
                        },
                        {
                            "com.ssn.simulation.entities.ConnectorPCXConnection": {
                                "name": "2",
                                "commandPort": 9201,
                                "statusPort": 8788
                            }
                        }
                    ],
                    "logSendOnStatusChannels": False
                }
            },
            {
                "com.ssn.simulation.entities.PCXPBLController": {
                    "id": "PCXPBLController4",
                    "posx": -3.0,
                    "posy": 6.8,
                    "sizex": 1.0,
                    "sizey": 1.0,
                    "sizez": 1.0,
                    "transparent": True,
                    "lastUpdate": 1560250110035,
                    "controllerId": "1"
                }
            }
        ])

        # Add PblGadget entities if light lines are selected
        if light_line_gadgets:
            gadget_entities = self._build_pbl_gadgets(light_line_gadgets)
            entities.extend(gadget_entities)

        # Core settings taken from the example WEC file (logimat_pbl.json)
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
                "statistics": {
                    "TranslateAction": 76.0,
                    "DeleteRelinkAction": 1.0,
                    "PasteAction": 4.0,
                    "CreateEntityAction": 13.0,
                    "DeleteAction": 8.0,
                    "EditAction": 60.0,
                    "CutAction": 1.0,
                },
                "lastUpdate": 0,
                "lastUpdateTitle": "WEC 3.2.0",
                "textAntialiasing": False,
            }
        }

        return json.dumps(core, indent=4)

    # ------------------------------------------------------------------
    # LOGIMAT ENTITY BUILDER
    # ------------------------------------------------------------------
    def _build_logimat(self, machine):
        """
        Build a { "com.ssn.simulation.entities.Logimat": {...} }
        matching the full WEC schema.
        """

        trays = [self._build_tray(t) for t in machine.trays]
        
        # Always create exactly 4 openings - use real data if available, otherwise disabled placeholders
        # Calculate absolute positions: start at 800, add 2000 for each opening on the same rack side
        openings_data = []
        for i in range(4):
            if i < len(machine.openings):
                opening = machine.openings[i]
                # Calculate absolute position based on rack side grouping
                rack_side = opening.rackSide
                # Count how many openings come before this one on the same rack side
                position_on_side = sum(1 for o in machine.openings[:i+1] if o.rackSide == rack_side)
                absolute_pos = 800 + ((position_on_side - 1) * 2000)
                openings_data.append((opening, absolute_pos))
            else:
                openings_data.append((None, 800 + (i * 2000)))  # Disabled openings get sequential positions
        
        openings = []
        for opening_data in openings_data:
            if opening_data[0] is not None:
                openings.append(self._build_opening(opening_data[0], opening_data[1]))
            else:
                openings.append(self._build_disabled_opening(opening_data[1]))

        return {
            "com.ssn.simulation.entities.Logimat": {
                "id": machine.id,
                "posx": machine.posx,
                "posy": machine.posy,
                "sizex": 3.0,
                "sizey": 200.0,
                "sizez": 1.0,
                "transparent": False,
                "lastUpdate": 0,

                # Communication
                "senderId": machine.senderId,
                "receiverId": machine.receiverId,
                "senderPort": machine.senderPort,
                "receiverPort": machine.receiverPort,

                # Machine physical parameters
                "trayWidth": machine.trays[0].trayLength if machine.trays else 815,
                "trayLength": machine.trays[0].trayWidth if machine.trays else 4025,
                "numberOfOpenings": len(machine.openings),
                "numberOfTrays": len(trays),
                "supportDistance": machine.supportDistance,
                "openingSupportDistance": machine.openingSupportDistance,
                "openingSupports": getattr(machine, "openingSupports", 6),
                "supportsFront": machine.supportsFront,
                "supportsRear": machine.supportsRear,
                "openingHeight": machine.openingHeight,
                "measuredHeight": getattr(machine, "measuredHeight", 0),
                "measuredWeight": getattr(machine, "measuredWeight", 0),
                "maximumHeight": machine.maximumHeight,
                "maximumWeight": machine.maximumWeight,
                "plcId": machine.plcId,
                "defaultMeasuredHeight": getattr(machine, "defaultMeasuredHeight", 0),
                "defaultMeasuredWeight": getattr(machine, "defaultMeasuredWeight", 0),

                # Motion settings
                "horizontalSpeed": machine.horizontalSpeed,
                "verticalSpeed": machine.verticalSpeed,
                "horizontalAcceleration": machine.horizontalAcceleration,
                "verticalAcceleration": machine.verticalAcceleration,
                "horizontalDeceleration": machine.horizontalDeceleration,
                "verticalDeceleration": machine.verticalDeceleration,
                "globalSpeedSetting": machine.globalSpeedSetting,

                # Additional height/elevator settings
                "logimatHeightMM": getattr(machine, "logimatHeightMM", 0),
                "startElevator": getattr(machine, "startElevator", 0),
                "endElevator": getattr(machine, "endElevator", 0),

                # Lists
                "trays": trays,
                "openings": openings,

                # Misc flags
                "columnXmm": getattr(machine, "columnXmm", [0, 0, 0]),
                "autoOn": getattr(machine, "autoOn", True),
                "errorState": getattr(machine, "errorState", False),
                "hasLogiBar": getattr(machine, "hasLogiBar", False),
            }
        }

    # ------------------------------------------------------------------
    # TRAY BUILDER
    # ------------------------------------------------------------------
    def _build_tray(self, tray):
        """
        Build a { "com.ssn.simulation.entities.LogimatTray": {...} }
        using the exact schema from example JSON.
        """
        return {
            "com.ssn.simulation.entities.LogimatTray": {
                "trayNo": tray.trayNo,
                "status": tray.status,
                "maximumLoad": tray.maxLoad,
                "trayWeight": tray.maxLoad,
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

    # ------------------------------------------------------------------
    # OPENING BUILDER
    # ------------------------------------------------------------------
    def _build_opening(self, opening, absolute_position):
        """
        Build an opening entry using full WEC expected fields.
        """

        return {
            "com.ssn.simulation.entities.LogimatOpening": {
                "side": opening.rackSide,
                "absolutePosition": absolute_position,
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

    def _build_disabled_opening(self, absolute_position):
        """
        Build a disabled opening entry for missing openings.
        """
        return {
            "com.ssn.simulation.entities.LogimatOpening": {
                "side": 0,
                "absolutePosition": absolute_position,
                "pointer": False,
                "stubStatus": False,
                "lightStatus": False,
                "tiltStatus": False,
                "safeStatus": False,
                "blockStatus": False,
                "pointerX": 0,
                "pointerZ": 0,
                "pointerHeight": 0,
                "liftPosition": 0,
                "lightMode": 0,
                "lightTimeout": 0,
                "popup": False,
                "openingOperationMode": 1,
            }
        }

    def _build_pbl_gadgets(self, gadgets):
        """
        Build PblGadget entities from database data.
        Position them starting at posx: -5.9, posy: 8.1
        Increment posx by 1 for each gadget on the same line
        Increment posy by 1 for new lines
        """
        entities = []

        # Group gadgets by line
        gadgets_by_line = {}
        for gadget in gadgets:
            line_id = gadget[1]  # line_lineId
            if line_id not in gadgets_by_line:
                gadgets_by_line[line_id] = []
            gadgets_by_line[line_id].append(gadget)

        # Sort lines
        sorted_lines = sorted(gadgets_by_line.keys())

        current_posy = 8.1
        gadget_id_counter = 1

        for line_id in sorted_lines:
            line_gadgets = gadgets_by_line[line_id]
            # Sort gadgets within line by gadgetId
            line_gadgets.sort(key=lambda g: g[0])  # gadgetId

            current_posx = -5.9

            for gadget in line_gadgets:
                entity = {
                    "com.ssn.simulation.entities.PblGadget": {
                        "id": f"PblGadget{gadget_id_counter}",
                        "posx": current_posx,
                        "posy": current_posy,
                        "sizex": 0.8,
                        "sizey": 0.8,
                        "sizez": 1.0,
                        "transparent": False,
                        "lastUpdate": 1560250160723,  # Using example timestamp
                        "controllerId": "1",
                        "lineNumber": str(line_id),
                        "addressNumber": str(gadget[0]),  # gadgetId
                        "activeOrderAck": True,
                        "responseTimeout": 0,
                        "confirmationDeviation": 0,
                        "aisle": 0,
                        "x": 0,
                        "y": 0,
                        "side": 0,
                        "pickLocationName": "WP01X01Y01",  # Default values
                        "workplaceName": "WP01",
                        "pickFace": False,
                        "gadgetType": "PBL"
                    }
                }
                entities.append(entity)

                current_posx += 1.0  # Increment posx for next gadget on same line
                gadget_id_counter += 1

            current_posy += 1.0  # Increment posy for next line

        return entities