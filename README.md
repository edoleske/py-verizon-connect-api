# Verizon Connect API
This module handles authentication and data-fetching with the Verizon 
Connect API. Currently, Verizon Connect uses the "Basic" HTTP 
authentication scheme, which requires a username and password. Use of 
the API will require registration of an app in their Developer Portal.

This project is not associated in any way with Verizon or Verizon Connect.

## Usage

First, register an app with Verizon Connect through the 
[Developer Portal](https://fim.us.fleetmatics.com/#/home/customlanding). 
You will receive a username, password and app ID to connect to the API with. 
Every endpoint is a public method in the API class.

```python
from verizon_connect_api import VerizonConnectAPI

api = VerizonConnectAPI(app_id, username, password)
vehicles = api.vehicles()
```

API errors will occur as the `HTTPError` exception from the `requests` 
library. These can be caught for exception handling.

```python
try:
    location = api.vehicle_location(vehicle_number)
except HTTPError as e:
    if e.response_code == 404:
        print("Vehicle not found!")
```

## Resources

Documentation: https://edoleske.github.com/py-verizon-connect-api

Verizon Connect API Terms and Conditions: https://fim.us.fleetmatics.com/content/home/landing/eapaas_agreement.html

