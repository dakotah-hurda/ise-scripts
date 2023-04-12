import requests
import sys


def find_endgr_id(ise_api_creds: str, search_string: str):
    """
    This function finds and returns an ISE ID Group based on the name provided search_string.
    """

    url = f"https://ISE-URL-GOES-HERE/ers/config/endpointgroup/name/{search_string}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {ise_api_creds}",
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        endgroup_data = response.json()
        endgroup_id = endgroup_data["EndPointGroup"]["id"]

        return endgroup_id

    else:
        print(f"ERROR: The API call to ISE failed. Error code: {response.status_code}")
        sys.exit(1)
