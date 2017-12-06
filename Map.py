from Car import Car
from func import add_nodes, clear, most_common
import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from descartes import PolygonPatch
from random import random, choice


ox.config(log_file=True, log_console=True, use_cache=True)
# Link to open street map
print "Enter https://www.openstreetmap.org/#map=17/39.74302/-105.52421 \n"

# Creating 2 police cars and 1 robbers car
p1, r1 = Car(20, 1), Car(20, 0.25)

################################################################################################

if raw_input("Based on bounding box [y],[n]: ") == "y":
    # For Idaho Springs
    #north, south, east, west = 39.7583, 39.7275, -105.4652, -105.5410
    # For Batory
    north, south, east, west = 52.2284, 52.2194, 21.0470, 21.0270
    # For Mokotow
    #north, south, east, west = 52.1905, 52.1791, 21.0657, 21.0497

    G = ox.graph_from_bbox(north, south, east, west, network_type='drive')
else:  # Creating graph based on place

    #place = raw_input("Enter place: ")
    #place = "Idaho Springs, USA"
    place = "srodmiescie, Warsaw, Poland"
    #place = "mokotow, Warsaw, Poland"

    G = ox.graph_from_place(place, network_type='drive')


# cords for start desitantion
#x, y = (39.74356, -105.52440)
# cords for mokotow
#x, y = (52.18576, 21.06227)
# cords fo Batory
x, y = (52.22194, 21.03446)

# setting nearest starting node
starting_node = ox.get_nearest_node(G, (x, y))
print "Starting node id: ", starting_node


# Creating exit nodes array
exit_nodes = []

if raw_input("Do you want to use predifined exit nodes? [y],[n]: ") == 'y':
    # Defined exit nodes Idaho Springs
    exit_nodes = [176598973, 176493948, 1410414960,
                  176567940, 176590273, 176557759, 176544697, 176472449]
    # Defined exit nodes for Srodmiescie
    #exit_nodes = []
    # Defined exit nodes for Mokotow
    #exit_nodes = []
else:
    # Randomly selected exit nodes based on degree level
    for x in G.nodes():
        if len(exit_nodes) >= 200:
            break
        if nx.degree(G, x) == 2 and nx.has_path(G, starting_node, x) == True:
            exit_nodes.append(x)

    # Using function from func.py
    add_nodes("exit nodes", exit_nodes)

################################################################################################


clear()
print "Exit nodes count: ", len(exit_nodes)

# Randomly setting destination node for robber
destination_node = choice(exit_nodes)
while nx.has_path(G, starting_node, destination_node) == False:
    destination_node = choice(exit_nodes)

print "Destination node id: ", destination_node

# Printing length of route in kilometeres
print "Path length: %s km!" % (nx.shortest_path_length(G, starting_node, destination_node, weight='length') / 1000)

# Calculation path times
path_times = r1.calculatePathTime(G, r1.returnRoute(
    G, starting_node, destination_node), starting_node)

# Creating best nodes array and defining route from return route
best_nodes = []
route = r1.returnRoute(G, starting_node, destination_node)


for m in G.nodes():
    if len(best_nodes) >= 50:
        break
    # If node is in route we need to delete it
    if m in r1.returnRoute(G, starting_node, destination_node):
        continue
    else:
        for n in range(0, len(r1.returnRoute(G, starting_node, destination_node))):
            if nx.has_path(G, m, route[n]) == True:
                if p1.pathTime(G, m, route[n]) <= path_times[n]:
                    best_nodes.append((m, route[n]))
                    # if we find good one we won't to exit second loop
                    break

for b in best_nodes:
    if raw_input("Proceed? [y],[n]: ") == 'y':
        # Showing full robbers path
        r1.ShowShortestPath(G, starting_node, destination_node)
        # Showing break point of robbers
        r1.ShowShortestPath(G, starting_node, b[1])
        # Showing break point of police
        p1.ShowShortestPath(G, b[0], b[1], 1)
        clear()
    else:
        break

b = most_common(best_nodes)

print "Best starting point for police: "
r1.ShowShortestPath(G, starting_node, starting_node, False, 8)
p1.ShowShortestPath(G, b[0], b[0], True, 8)
