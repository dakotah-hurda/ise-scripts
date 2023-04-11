import json
import requests
from pprint import pprint


def create_endpoint(ise_api_creds: str, endpoint_mac: str):
    """
    This function takes the provided MAC address and creates a new static endpoint on ISE.
    """

    url = f"https://cise520lpi3.milwaukeecountywi.gov/ers/config/endpoint"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {ise_api_creds}",
    }

    data = {
        "ERSEndPoint": {
            "name": endpoint_mac,
            "description": "Created automatically via Python script",
            "mac": endpoint_mac,
        }
    }

    data = json.dumps(data)

    response = requests.request("POST", url, headers=headers, data=data)

    if response.status_code == 201:  # TODO #5
        return True
    else:
        return False
