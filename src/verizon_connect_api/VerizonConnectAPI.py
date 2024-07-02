import requests

from base64 import b64encode
from datetime import datetime, timezone
from urllib.parse import quote


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
    :param endpoint: API endpoint, defaults to 'https://fim.api.us.fleetmatics.com:443/'
    :type endpoint: str
    """

    def __init__(self, app_id: str, username: str, password: str, endpoint='https://fim.api.us.fleetmatics.com:443/'):
        self._URL_BASE = endpoint
        self._APP_ID = app_id

        encoded_credentials = b64encode(f"{username}:{password}".encode("utf-8"))
        self._BASIC_AUTH_HEADER = f'Basic {encoded_credentials.decode("utf-8")}'
        self._token = self._get_token()

    def vehicles(self):
        return self._json_request(f"cmd/v1/vehicles")

    def activated_tcs(self):
        return self._json_request(f"rad/v1/vehicles/getvehiclesactivedtcs")

    def gps_history(self, vehicle_number: str, start: datetime, end: datetime):
        if datetime.now(timezone.utc) < start:
            raise ValueError('Start datetime cannot be in the future')

        if not start < end:
            raise ValueError('Start datetime must be before end datetime')

        return self._json_request(
            f"rad/v1/vehicles/{vehicle_number}/status/"
            f"history?startdatetimeutc={self._format_date(start)}&enddatetimeutc={self._format_date(end)}")

    def segment_data(self, vehicle_number: str, start: datetime):
        if datetime.now(timezone.utc) < start:
            raise ValueError('Start datetime cannot be in the future')

        return self._json_request(
            f"rad/v1/vehicles/{vehicle_number}/segments?startdateutc={self._format_date(start)}")

    def vehicle_dtc_history(self, vehicle_number: str):
        return self._json_request(f"rad/v1/vehicles/{vehicle_number}/getdtchistorybyvehiclenumber")

    def vehicle_ecm_status(self, vehicle_number: str):
        return self._json_request(f"rad/v1/vehicles/{vehicle_number}/getecmstatusbyvehiclenumber")

    def vehicle_location(self, vehicle_number: str):
        return self._json_request(f"rad/v1/vehicles/{vehicle_number}/location")

    def vehicle_status(self, vehicle_number: str):
        return self._json_request(f"rad/v1/vehicles/{vehicle_number}/status")

    def _json_request(self, endpoint, retry=1):
        """Fetches endpoint request and parses response to JSON"""
        # API requires encoding for whitespace and characters '"#%|&-<>()'
        encoded_endpoint = quote(endpoint).replace("-", "%2D")
        response = requests.get(f'{self._URL_BASE}{encoded_endpoint}', headers={
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
    def _format_date(date: datetime) -> str:
        """Formats and validates a date for endpoint URLs"""
        if not date.tzinfo == timezone.utc:
            raise ValueError('Verizon Connect API only accepts UTC datetimes')

        return date.strftime('%Y-%m-%dT%H:%M:%S')
