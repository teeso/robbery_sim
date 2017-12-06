from Car import Car
import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from descartes import PolygonPatch

ox.config(log_file=True, log_console=True, use_cache=True)
# Link to open street map
print "Enter https://www.openstreetmap.org/#map=17/39.74302/-105.52421 \n"

# Creating robber car
r1 = Car(50, 0.25)

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

    #place = raw_input("Enter place: " )
    #place = "Idaho Springs, USA"
    place = "srodmiescie, Warsaw, Poland"
    #place = "mokotow, Warsaw, Poland"

    G = ox.graph_from_place(place, network_type='drive')


# cords for Idaho Springs
#x, y = (39.74356, -105.52440)
# cords for mokotow
#x, y = (52.18576, 21.06227)
# cords fo Batory
x, y = (52.22194, 21.03446)

################################################################################################

# Setting nearest starting node
starting_node = ox.get_nearest_node(G, (x, y))
print "Starting node id: ", starting_node

# 5,10,15,20,25
# Minutes from beginning
list_of_ints = list(range(1, 25, 5))
escape_time = list_of_ints

# Setting robber ar travelling speed
meters_per_minute = r1.car_speed * 1000 / 60
for u, v, k, data in G.edges(data=True, keys=True):
    data['time'] = data['length'] / meters_per_minute

# Get one color for each isochrone
iso_colors = ox.get_colors(
    n=len(escape_time), cmap='GnBu', start=0.3, return_hex=True)

# Make the isochrone polygons
isochrone_polys = []
for trip_time in sorted(escape_time, reverse=True):
    subgraph = nx.ego_graph(
        G, starting_node, radius=trip_time, distance='time')
    node_points = [Point((data['x'], data['y']))
                   for node, data in subgraph.nodes(data=True)]
    bounding_poly = gpd.GeoSeries(node_points).unary_union.convex_hull
    isochrone_polys.append(bounding_poly)

# Plot the network then add isochrones as colored descartes polygon patches
fig, ax = ox.plot_graph(G, fig_height=8, show=False, close=False,
                        edge_color='k', edge_alpha=0.2, node_color='none')
for polygon, fc in zip(isochrone_polys, iso_colors):
    patch = PolygonPatch(polygon, fc=fc, ec='none', alpha=0.6, zorder=-1)
    ax.add_patch(patch)
plt.show()
