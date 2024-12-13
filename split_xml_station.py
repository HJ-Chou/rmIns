# ----------------------------------------------------------------------------------------------------
# HJC
# IESDMC
# 2024-12-11
# ver1.0
# ----------------------------------------------------------------------------------------------------
import os
import sys
from obspy import read_inventory


# ensure the input
if len(sys.argv) != 2:
    print("Usage: python split_xml_station.py <xml file>")
    sys.exit(1)

# input xml file
input_xml_path = str(sys.argv[1])

# inv
inv = read_inventory(input_xml_path)

# mk xml folder if not exist
dirs = './xml'  # to store the splited xml file
if not os.path.exists(dirs):
    os.makedirs(dirs)

# split the xml
for network in inv:
    for station in network:
        inv_single = inv.select(network=network.code, station=station.code)
        inv_single.write(f"./xml/{station.code}.xml", format="STATIONXML")

