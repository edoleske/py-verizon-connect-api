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


class VerizonConnectAPITestCase(TestCase):
    def setUp(self):
        load_dotenv()
        app_id = os.getenv('APP_ID')
        app_user = os.getenv('API_USERNAME')
        app_pass = os.getenv('API_PASSWORD')

        self.api = VerizonConnectAPI(app_id, app_user, app_pass)
        self.assertIsInstance(self.api, VerizonConnectAPI)


class TestDriversAPI(VerizonConnectAPITestCase):
    def setUp(self):
        super().setUp()

        drivers = self.api.drivers()
        self.assertIsInstance(drivers, list)
        self.assertGreater(len(drivers), 0, "At least one driver needed to test driver APIs.")
        driver_details = drivers[0]['Driver']
        self.assertIsInstance(driver_details, dict)
        self.driver_number = driver_details['DriverNumber']
        self.assertTrue(self.driver_number is not None and len(self.driver_number) > 0,
                        f'{self.driver_number} is not a valid driver number for testing.')

    def test_drivers(self):
        drivers = self.api.drivers()
        self.assertIsInstance(drivers, list)

        driver_validator = validator_from_type(Driver)
        for driver in drivers:
            driver_validator.validate_python(driver, strict=True)

    def test_driver(self):
        driver = self.api.driver(self.driver_number)
        driver_validator = validator_from_type(Driver)
        driver_validator.validate_python(driver, strict=True)

    def test_driver_keys(self):
        keys = self.api.driver_keys(self.driver_number)
        self.assertIsInstance(keys, list)
        for key in keys:
            self.assertIsInstance(key, str)

    def test_driver_logbook_settings(self):
        settings = self.api.driver_logbook_settings(self.driver_number)
        logbook_settings_validator = validator_from_type(DriverLogBookSettingsResponse)
        logbook_settings_validator.validate_python(settings, strict=True)

    def test_driver_segments(self):
        start = datetime.now(timezone.utc) - timedelta(days=1)

        segments = self.api.driver_segments(self.driver_number, start)
        self.assertIsInstance(segments, list)

        segment_validator = validator_from_type(SegmentHistory)
        for segment in segments:
            segment_validator.validate_python(segment, strict=True)


class TestVehiclesAPI(VerizonConnectAPITestCase):
    def setUp(self):
        super().setUp()

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
        for vehicle in vehicles:
            vehicle_validator.validate_python(vehicle, strict=True)

    def test_vehicle(self):
        vehicle = self.api.vehicle(self.vehicle_number)
        vehicle_validator = validator_from_type(Vehicle)
        vehicle_validator.validate_python(vehicle, strict=True)

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


class TestUsersAPI(VerizonConnectAPITestCase):
    def setUp(self):
        super().setUp()

        users = self.api.users()
        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0, "At least one vehicle needed to test vehicle APIs.")

        for user in users:
            user_details = user['user']
            self.assertIsInstance(user_details, dict)
            self.employee_id = user_details['EmployeeId']
            if self.employee_id is not None:
                break
        self.assertTrue(self.employee_id is not None, "No employee IDs found to test user APIs.")

    def test_users(self):
        users = self.api.users()
        self.assertIsInstance(users, list)

        user_validator = validator_from_type(UserResponse)
        for user in users:
            user_validator.validate_python(user, strict=True)

    def test_user(self):
        user = self.api.user(self.employee_id)
        user_validator = validator_from_type(UserResponse)
        user_validator.validate_python(user, strict=True)
