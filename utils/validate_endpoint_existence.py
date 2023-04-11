import requests
import sys
from pprint import pprint


def validate(test_mac: str, ise_api_creds: str):
    """
    This function checks if the provided MAC address exists as a known endpoint in ISE.

    Returns boolean,endpoint_id
    """

    url = "https://cise520lpi3.milwaukeecountywi.gov/ers/config/endpoint"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {ise_api_creds}",
    }

    params = {
        "filter": f"mac.EQ.{test_mac}",
    }

    response = requests.request("GET", url, headers=headers, params=params)

    resp_data = response.json()

    endpoint_count = resp_data["SearchResult"]["total"]

    if endpoint_count == 1:
        endpoint_id = resp_data["SearchResult"]["resources"][0]["id"]
        return True, endpoint_id  # Endpoint exists

    elif endpoint_count == 0:
        endpoint_id = ""
        return False, endpoint_id  # Endpoint does not exist

    else:
        print(  # TODO #4
            "ERROR: Multiple endpoints exist. Not sure how this happened. Investigate!"
        )
        print(f"MAC Address in question: {test_mac}")
        sys.exit(1)
