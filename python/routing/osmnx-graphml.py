import osmnx as ox
import time
import os


#Get graphml from Overpass api
def place_to_graphml(place, graphml_file):
    G = ox.graph_from_place(place,network_type="drive")
    ox.save_load.save_graphml(G, graphml_file)
    
#Get grpahml from local .osm file
def osm_to_graphml(osm_file, graphml_file):
    G = ox.graph_from_file(place,network_type="drive")
    ox.save_load.save_graphml(G, graphml_file)

place_to_graphml("Helsinki, Finland", "helsinki.graphml")
osm_to_graphml("finland-latest.osm", "finland.graphml")
