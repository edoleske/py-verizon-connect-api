import os

from unittest import TestCase
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from typing import Any
from pydantic import TypeAdapter, ConfigDict
from verizon_connect_api.VerizonConnectAPI import VerizonConnectAPI
from verizon_connect_api.api_types import *


def validator_from_type(source: Any) -> TypeAdapter:
    source.__pydantic_config__ = ConfigDict(extra='forbid')
    return TypeAdapter(source)


class TestVerizonConnectVehiclesAPI(TestCase):
    def setUp(self):
        load_dotenv()
        app_id = os.getenv('APP_ID')
        app_user = os.getenv('API_USERNAME')
        app_pass = os.getenv('API_PASSWORD')

        self._pydantic_config = ConfigDict(extra='forbid')

        self.api = VerizonConnectAPI(app_id, app_user, app_pass)
        self.assertIsInstance(self.api, VerizonConnectAPI)

        vehicles = self.api.vehicles()
        self.assertIsInstance(vehicles, list)
        self.assertGreater(len(vehicles), 0, "At least one vehicle needed to test vehicle APIs.")
        self.vehicle_number = vehicles[0]['VehicleNumber'].rstrip()
        self.assertTrue(self.vehicle_number is not None and len(self.vehicle_number) > 0,
                        f'{self.vehicle_number} is not a valid vehicle number for testing.')

    def test_vehicles(self):
        vehicles = self.api.vehicles()
        self.assertIsInstance(vehicles, list)

        vehicle_validator = validator_from_type(Vehicle)
        for test_vehicle in vehicles:
            vehicle_validator.validate_python(test_vehicle, strict=True)

    def test_active_dtcs(self):
        active_dtcs = self.api.active_dtcs()
        self.assertIsInstance(active_dtcs, list)

        active_dtc_validator = validator_from_type(ActiveDiagnosticTroubleCodes)
        for active_dtc in active_dtcs:
            active_dtc_validator.validate_python(active_dtc, strict=True)

    def test_gps_history(self):
        start = datetime.now(timezone.utc) - timedelta(days=1)
        end = datetime.now(timezone.utc)

        gps_history = self.api.vehicle_gps_history(self.vehicle_number, start, end)
        self.assertIsInstance(gps_history, list)

        gps_validator = validator_from_type(VehicleGPSLocation)
        for gps_location in gps_history:
            gps_validator.validate_python(gps_location, strict=True)

    def test_segments(self):
        start = datetime.now(timezone.utc) - timedelta(days=1)

        segments = self.api.vehicle_segments(self.vehicle_number, start)
        self.assertIsInstance(segments, list)

        segment_validator = validator_from_type(SegmentHistory)
        for segment in segments:
            segment_validator.validate_python(segment, strict=True)

    def test_dtc_history(self):
        dtc_history = self.api.vehicle_dtc_history(self.vehicle_number)
        dtc_history_validator = validator_from_type(DiagnosticTroubleCodeHistory)
        dtc_history_validator.validate_python(dtc_history, strict=True)

    def test_ecm_status(self):
        ecm_status = self.api.vehicle_ecm_status(self.vehicle_number)
        ecm_status_validator = validator_from_type(EngineControlModuleStatus)
        ecm_status_validator.validate_python(ecm_status, strict=True)

    def test_location(self):
        location = self.api.vehicle_location(self.vehicle_number)
        location_validator = validator_from_type(LocationStatus)
        location_validator.validate_python(location, strict=True)

    def test_status(self):
        status = self.api.vehicle_status(self.vehicle_number)
        status_validator = validator_from_type(VehicleStatus)
        status_validator.validate_python(status, strict=True)
