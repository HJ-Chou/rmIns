import os
from obspy import read_inventory

dirs = './xml'
if not os.path.exists(dirs):
    os.makedirs(dirs)

inv = read_inventory('./CWASN.stationXML')

for network in inv:
    for station in network:
        inv_single = inv.select(network=network.code, station=station.code)
        inv_single.write(f"./xml/{station.code}.xml", format="STATIONXML")

