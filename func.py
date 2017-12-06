import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from descartes import PolygonPatch
from random import random, choice
import os


def add_nodes(type_of_node_text, node_array):
    # If user want to add asome addiotnal exit_nodes
    while raw_input("Do you want to enter more %s ? [y],[n]: " % (type_of_node_text)) == 'y':
        # Spliting by first blank space
        x, y = raw_input("Enter two coordinates: ").split()
        # Chosing the nearest node from point
        node_array.append(ox.get_nearest_node(G, (x, y)))


def clear():
    os.system('clear')


def most_common(lst):
    return max(set(lst), key=lst.count)
