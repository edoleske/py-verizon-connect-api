import os

from unittest import TestCase
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from verizon_connect_api.VerizonConnectAPI import VerizonConnectAPI


class TestVerizonConnectVehiclesAPI(TestCase):
    def setUp(self):
        load_dotenv()
        app_id = os.getenv('APP_ID')
        app_user = os.getenv('API_USERNAME')
        app_pass = os.getenv('API_PASSWORD')

        self.api = VerizonConnectAPI(app_id, app_user, app_pass)
        self.assertIsInstance(self.api, VerizonConnectAPI)

        vehicles = self.api.vehicles()
        self.assertIsInstance(vehicles, list)
        self.assertGreater(len(vehicles), 0, "At least one vehicle needed to test vehicle APIs.")
        self.vehicle_number = vehicles[0]['VehicleNumber'].rstrip()

    def test_vehicles(self):
        vehicles = self.api.vehicles()
        for test_vehicle in vehicles:
            self.assertIsInstance(test_vehicle, dict)
            self.assertIn('Name', test_vehicle)
            self.assertIsInstance(test_vehicle['Name'], str)
            self.assertIn('VehicleNumber', test_vehicle)
            self.assertTrue(test_vehicle['VehicleNumber'] is None or isinstance(test_vehicle['VehicleNumber'], str))

    def test_activated_tcs(self):
        activated_tcs = self.api.activated_tcs()
        self.assertIsInstance(activated_tcs, list)

    def test_gps_history(self):
        start = datetime.now(timezone.utc) - timedelta(days=1)
        end = datetime.now(timezone.utc)

        gps_history = self.api.gps_history(self.vehicle_number, start, end)
        self.assertIsInstance(gps_history, list)

    def test_segment_data(self):
        start = datetime.now(timezone.utc) - timedelta(days=1)

        segment_data = self.api.segment_data(self.vehicle_number, start)
        self.assertIsInstance(segment_data, list)

    def test_dtc_history(self):
        dtc_history = self.api.vehicle_dtc_history(self.vehicle_number)
        self.assertIsInstance(dtc_history, dict)

    def test_ecm_status(self):
        ecm_status = self.api.vehicle_ecm_status(self.vehicle_number)
        self.assertIsInstance(ecm_status, dict)

    def test_location(self):
        location = self.api.vehicle_location(self.vehicle_number)
        self.assertIsInstance(location, dict)

    def test_status(self):
        status = self.api.vehicle_status(self.vehicle_number)
        self.assertIsInstance(status, dict)
