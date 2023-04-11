# Cityworks ISE Scripts

This folder is used for storing scripts relevant for interacting with Cityworks iPads. 

# cityworks_idgr_addmacs.py

## Overview

The primary script here is cityworks_idgr_addmacs.py which is used for adding provided MAC addresses to the Cityworks-iPads ID Group on ISE. 

The script handles:

- Filtering out MACs that are already in the group
- Creating endpoints for MACs that don't already exist on ISE
- Automatically assigning each endpoint to the correct group

## Pre-Requisites
- Configure a .env file in the local or root directory with the following information: 

    - ise_ers_username="ers-username-goes-here"
    - ise_ers_password="ers-password-goes-here"

- Populate the 'new-macs.csv' file with the MACs you want to add to the Cityworks-iPads ID group. Put everything in the first column and one MAC per row.



