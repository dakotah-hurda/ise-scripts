import requests
import sys
from pprint import pprint


def retrieve_endgr_hosts(ise_api_creds: str, endgr_id: str):
    """
    This function finds and returns hosts in the specified ISE Endpoint ID Group.
    """
    hosts_list = []

    url = "https://cise520lpi3.milwaukeecountywi.gov/ers/config/endpoint"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {ise_api_creds}",
    }

    params = {
        "filter": f"groupId.EQ.{endgr_id}",
        "size": "100",  # Asks for 100 results per page.
    }

    # ----------------------------------------------------- #
    # This section handles looping through response pages.  #
    # ISE can only support up to 100 responses per 'page',  #
    # so need to cycle through them until we hit the end.   #
    # ----------------------------------------------------- #

    last_page = False
    while not last_page:
        response = requests.request("GET", url, headers=headers, params=params)
        if response.status_code == 200:
            resp_data = response.json()

            for host in resp_data["SearchResult"]["resources"]:
                hosts_list.append(host["name"])

            if "nextPage" in resp_data["SearchResult"].keys():
                url = resp_data["SearchResult"]["nextPage"]["href"]

            else:
                last_page = True
        else:
            print(
                "ERROR: Something broke when trying to reach the ISE API inside the retrieve_endgr_hosts function."
            )
            print(f"Status code: {response.status_code}")
            sys.exit(1)

    return hosts_list
