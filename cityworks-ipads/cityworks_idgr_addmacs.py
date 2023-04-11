# Standard Library Modules
import csv
from dotenv import load_dotenv
from pprint import pprint
import os


# Custom Modules
from utils import (
    base64_encode,
    find_endgr_id,
    retrieve_endgr_hosts,
    validate_endpoint_existence,
    update_endgr,
    create_endpoint,
)


def import_new_macs():
    """
    This function reads in the MACs provided in the local .CSV file, 'new-macs.csv'.
    """

    new_macs = []

    with open("new-macs.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=" ")

        for row in reader:
            new_macs.append(row[0])

    return new_macs


def remove_dup_macs(endgr_macs: list, new_mac_list: list):
    """
    This function compares the provided lists of MACs in the endpoint group and the list
    of MACs that we wish to add TO that group. Returns the filtered list of MACs.
    """
    dup_macs = []
    new_macs = []

    for new_mac in new_mac_list:
        if new_mac in endgr_macs:
            dup_macs.append(new_mac)
        else:
            new_macs.append(new_mac)
            continue

    if len(dup_macs) > 0:
        print(
            f"INFO: The following MACs were found in the existing endpoint group and will not be added: \n\n{dup_macs}"
        )
    else:
        print("SUCCESS: No new MACs were found in the existing endpoint group.")

    return new_macs


def cityworks_idgr_addmacs():
    """
    This function is the high-level handler for retrieving and formatting all relevant data.

    Call this function directly.
    """

    # This section retrieves and formats your ISE API creds.
    load_dotenv()
    ise_username = os.environ.get("ise_ers_username")
    ise_password = os.environ.get("ise_ers_password")
    ise_api_creds = base64_encode.encode(f"{ise_username}:{ise_password}")

    # Read in the MAC addresses entered in the local .CSV.
    new_macs = import_new_macs()

    # Retrieve the endpoint group ID.
    endgroup_id = find_endgr_id.find_endgr_id(
        ise_api_creds=ise_api_creds,
        search_string="id_gr_cityworks_ipads_secure_wireless_static_vlan_155",
    )

    # Retrieve all hosts in the endpoint group.
    endgr_hosts = retrieve_endgr_hosts.retrieve_endgr_hosts(
        ise_api_creds=ise_api_creds,
        endgr_id=endgroup_id,
    )

    # Compare new_macs with MACs already found in ISE. Filter out duplicates.
    new_macs = remove_dup_macs(endgr_macs=endgr_hosts, new_mac_list=new_macs)

    for new_mac in new_macs:
        # Check all new_macs to see if we need to add a new endpoint for it on ISE before adding to the endpoint group.
        new_mac_bool, endpoint_id = validate_endpoint_existence.validate(
            test_mac=new_mac, ise_api_creds=ise_api_creds
        )

        # If the MAC endpoint already exists on ISE, add it to the right group.
        if new_mac_bool:
            update_endgr.update_endgr(
                endpoint_id=endpoint_id,
                ise_api_creds=ise_api_creds,
                endgr_id=endgroup_id,
            )

        # If the MAC endpoint does not already exist on ISE, create the new endpoint, then add to the right group.
        else:
            # Create new endpoint for the provided MAC.
            endpoint_create_bool = create_endpoint.create_endpoint(
                ise_api_creds=ise_api_creds, endpoint_mac=new_mac
            )

            if endpoint_create_bool:
                # Validate the new endpoint exists.
                new_mac_bool, endpoint_id = validate_endpoint_existence.validate(
                    test_mac=new_mac, ise_api_creds=ise_api_creds
                )

                # If the new endpoint exists, add it to the correct group.
                if new_mac_bool:
                    update_endgr.update_endgr(
                        endpoint_id=endpoint_id,
                        ise_api_creds=ise_api_creds,
                        endgr_id=endgroup_id,
                    )

                # TODO #3
                else:
                    print(f"ERROR: Failed validating new endpoint for MAC {new_mac}")
                    continue
            else:
                print(f"ERROR: Failed creating new endpoint for MAC {new_mac}")
                continue

    return ()


cityworks_idgr_addmacs()
