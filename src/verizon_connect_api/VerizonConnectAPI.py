import requests

from base64 import b64encode
from datetime import datetime, timezone
from urllib.parse import quote

from verizon_connect_api.api_types import *


class VerizonConnectAPI:
    """
    This module handles authentication and data-fetching with the Verizon Connect API. Currently, Verizon Connect uses
    the "Basic" HTTP authentication scheme, which requires a username and password. Use of the API will require
    registration of an app in their Developer Portal.

    :param app_id: ID of app registered in Verizon Connect Developer Portal
    :type app_id: str
    :param username: Username for account generated during app registration
    :type username: str
    :param password: Password for account generated during app registration
    :type password: str
    :param api_url: API endpoint, defaults to 'https://fim.api.us.fleetmatics.com:443/'
    :type api_url: str
    """

    def __init__(self, app_id: str, username: str, password: str, api_url='https://fim.api.us.fleetmatics.com:443/'):
        self._URL_BASE = api_url
        self._APP_ID = app_id

        encoded_credentials = b64encode(f"{username}:{password}".encode("utf-8"))
        self._BASIC_AUTH_HEADER = f'Basic {encoded_credentials.decode("utf-8")}'
        self._token = self._get_token()

    def drivers(self) -> list[Driver]:
        """
        Gets driver information for all drivers.

        **Endpoint:** ``cmd/v1/drivers``

        :return: List of dictionaries with driver details and links
        :rtype: list[Driver]
        """
        return self._json_request(f"cmd/v1/drivers")

    def driver(self, driver_number: str) -> Driver:
        """
        Gets driver information for a specific driver.

        **Endpoint:** ``cmd/v1/drivers/{driver_number}``

        :param driver_number: Driver number
        :type driver_number: str
        :return: Driver details and links
        :rtype: Driver
        """
        return self._json_request(f"cmd/v1/drivers/{self._format_string(driver_number)}")

    def driver_keys(self, driver_number: str) -> list[str]:
        """
        Gets driver's key fob IDs.

        **Endpoint:** ``cmd/v1/drivers/{driver_number}/keys``

        :param driver_number: Driver number
        :type driver_number: str
        :return: List of key fob IDs as strings
        :rtype: list[str]
        """
        return self._json_request(f"cmd/v1/drivers/{self._format_string(driver_number)}/keys")

    def driver_logbook_settings(self, driver_number: str) -> DriverLogBookSettingsResponse:
        """
        Gets driver's logbook settings.

        **Endpoint:** ``cmd/v1/driversettings/logbooksettings/{driver_number}``

        :param driver_number: Driver number
        :type driver_number: str
        :return: Driver logbook settings
        :rtype: DriverLogBookSettingsResponse
        """
        return self._json_request(f"cmd/v1/driversettings/logbooksettings/{self._format_string(driver_number)}")

    def driver_segments(self, driver_number: str, start: datetime) -> list[SegmentHistory]:
        """
        Gets driver's vehicles ignition start and stop times for 24-hour period

        **Endpoint:** ``rad/v1/drivers/{driver_number}/segments``

        :param driver_number: Driver number
        :type driver_number: str
        :param start: UTC datetime at start of 24-hour period
        :type start: datetime
        :return: List of dictionaries with driver information and list of segments
        :rtype: list[SegmentHistory]
        """
        if datetime.now(timezone.utc) < start:
            raise ValueError('Start datetime cannot be in the future')

        return self._json_request(
            f"rad/v1/drivers/{self._format_string(driver_number)}/segments?startdateutc={self._format_date(start)}")

    def users(self) -> list[UserResponse]:
        """
        Gets application users

        **Endpoint:** ``cmd/v1/users``

        :return: List of dictionaries with application user information
        :rtype: list[UserResponse]
        """
        return self._json_request(f"cmd/v1/users")

    def user(self, employee_id: int) -> UserResponse:
        """
        Gets application user

        **Endpoint:** ``cmd/v1/users/{employee_id}``

        :param employee_id: Employee ID, must be integer
        :type employee_id: int
        :return: Dictionary with user information
        :rtype: UserResponse
        """
        return self._json_request(f"cmd/v1/users/{employee_id}")

    def vehicles(self) -> list[Vehicle]:
        """
        Gets basic vehicle information for all vehicles.

        **Endpoint:** ``cmd/v1/vehicles``

        :return: List of dictionaries for each vehicle
        :rtype: list[Vehicle]
        """
        return self._json_request(f"cmd/v1/vehicles")

    def vehicle(self, vehicle_number: str) -> Vehicle:
        """
        Gets basic vehicle information for a specific vehicle.

        **Endpoint:** ``cmd/v1/vehicles/{vehicle_number}``

        :param vehicle_number: Vehicle number
        :type vehicle_number: str
        :return: Dictionary with vehicle details
        :rtype: Vehicle
        """
        return self._json_request(f"cmd/v1/vehicles/{self._format_string(vehicle_number)}")

    def active_dtcs(self) -> list[ActiveDiagnosticTroubleCodes]:
        """
        Gets active diagnostic trouble codes (DTCs) for all vehicles.

        **Endpoint:** ``rad/v1/vehicles/getvehiclesactivedtcs``

        :return: List of dictionaries for each vehicle with all active DTCs as string
        :rtype: list[ActiveDiagnosticTroubleCodes]
        """
        return self._json_request(f"rad/v1/vehicles/getvehiclesactivedtcs")

    def vehicle_gps_history(self, vehicle_number: str, start: datetime, end: datetime) -> list[VehicleGPSLocation]:
        """
        Gets GPS location history for a given vehicle.

        **Endpoint:** ``rad/v1/vehicles/{vehiclenumber}/status/history``

        :param vehicle_number: VehicleNumber of vehicle
        :type vehicle_number: str
        :param start: UTC datetime at start of time range
        :type start: datetime
        :param end: UTC datetime at end of time range
        :type end: datetime
        :return: List of dictionaries with timestamped GPS locations
        :rtype: list[VehicleGPSLocation]
        """
        if datetime.now(timezone.utc) < start:
            raise ValueError('Start datetime cannot be in the future')

        if not start < end:
            raise ValueError('Start datetime must be before end datetime')

        return self._json_request(
            f"rad/v1/vehicles/{self._format_string(vehicle_number)}/status/"
            f"history?startdatetimeutc={self._format_date(start)}&enddatetimeutc={self._format_date(end)}")

    def vehicle_segments(self, vehicle_number: str, start: datetime) -> list[SegmentHistory]:
        """
        Get a vehicle's ignition start and stop times for a 24-hour period.

        **Endpoint:** ``rad/v1/vehicles/{vehiclenumber}/segments``

        :param vehicle_number: VehicleNumber of vehicle
        :param start: UTC datetime at start of 24-hour period
        :type start: datetime
        :return: List of dictionaries with vehicle information and list of segments
        :rtype: list[SegmentHistory]
        """
        if datetime.now(timezone.utc) < start:
            raise ValueError('Start datetime cannot be in the future')

        return self._json_request(
            f"rad/v1/vehicles/{self._format_string(vehicle_number)}/"
            f"segments?startdateutc={self._format_date(start)}")

    def vehicle_dtc_history(self, vehicle_number: str) -> DiagnosticTroubleCodeHistory:
        """
        Gets diagnostic trouble code (DTC) history for a given vehicle.

        **Endpoint:** ``rad/v1/vehicles/{vehiclenumber}/getdtchistorybyvehiclenumber``

        :param vehicle_number: VehicleNumber of vehicle
        :type vehicle_number: str
        :return: Dictionary with vehicle information and list of DTCs
        :rtype: DiagnosticTroubleCodeHistory
        """
        return self._json_request(f"rad/v1/vehicles/{self._format_string(vehicle_number)}/"
                                  f"getdtchistorybyvehiclenumber")

    def vehicle_ecm_status(self, vehicle_number: str) -> EngineControlModuleStatus:
        """
        Gets status of vehicle's engine control module (ECM).

        **Endpoint:** ``rad/v1/vehicles/{vehiclenumber}/getecmstatusbyvehiclenumber``

        :param vehicle_number: VehicleNumber of vehicle
        :type vehicle_number: str
        :return: Dictionary with parameters from engine control module
        :rtype: EngineControlModuleStatus
        """
        return self._json_request(f"rad/v1/vehicles/{self._format_string(vehicle_number)}/"
                                  f"getecmstatusbyvehiclenumber")

    def vehicle_location(self, vehicle_number: str) -> LocationStatus:
        """
        Gets location information for a given vehicle.

        **Endpoint:** ``rad/v1/vehicles/{vehiclenumber}/location``

        :param vehicle_number: VehicleNumber of vehicle
        :return: Dictionary with vehicle location parameters
        :rtype: LocationStatus
        """
        return self._json_request(f"rad/v1/vehicles/{self._format_string(vehicle_number)}/"
                                  f"location")

    def vehicle_status(self, vehicle_number: str) -> VehicleStatus:
        """
        Gets vehicle status for a given vehicle.

        **Endpoint:** ``rad/v1/vehicles/{vehiclenumber}/status``

        :param vehicle_number: VehicleNumber of vehicle
        :return: Dictionary with vehicle status parameters
        :rtype: VehicleStatus
        """
        return self._json_request(f"rad/v1/vehicles/{self._format_string(vehicle_number)}/status")

    def _json_request(self, endpoint, retry=1):
        """Fetches endpoint request and parses response to JSON (assumes correct endpoint encoding)"""
        response = requests.get(f'{self._URL_BASE}{endpoint}', headers={
            'Authorization': f'Atmosphere atmosphere_app_id={self._APP_ID}, Bearer {self._token}',
            'Accept': 'application/json'})

        # Refresh token if expired
        if response.status_code == 400 and response.text == 'The provided token has an invalid format.':
            self._token = self._get_token()

        # Retry on error response (handles token expiration and occasional timeout)
        if response.status_code >= 400 and retry > 0:
            return self._json_request(endpoint, retry=retry-1)

        response.raise_for_status()
        return response.json()

    def _get_token(self):
        """Fetches access token using HTTP basic authentication"""
        endpoint = f'{self._URL_BASE}token'
        headers = {'Accept': 'text/plain', 'Authorization': self._BASIC_AUTH_HEADER}
        response = requests.get(endpoint, headers=headers)
        if not response.status_code == 200:
            raise RuntimeError(f'Error fetching token: {response.text}')
        return response.text

    @staticmethod
    def _format_string(parameter: str):
        """Formats string parameters for endpoint URLs"""
        return quote(parameter.rstrip()).replace('-', '%2D')

    @staticmethod
    def _format_date(date: datetime) -> str:
        """Formats and validates a date for endpoint URLs"""
        if not date.tzinfo == timezone.utc:
            raise ValueError('Verizon Connect API only accepts UTC datetimes')

        return quote(date.strftime('%Y-%m-%dT%H:%M:%S'))
