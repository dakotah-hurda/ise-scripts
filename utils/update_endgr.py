import requests
import json
from pprint import pprint


def update_endgr(endpoint_id: str, ise_api_creds: str, endgr_id: str):
    """
    This function handles adding the provided list of new_macs to the provided endpoint group.
    """

    url = f"https://ISE-URL-GOES-HERE/ers/config/endpoint/{endpoint_id}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {ise_api_creds}",
    }

    data = {"ERSEndPoint": {"groupId": endgr_id}}

    data = json.dumps(data)

    response = requests.request("PUT", url, headers=headers, data=data)

    pprint(response.status_code)
    pprint(response.json())
