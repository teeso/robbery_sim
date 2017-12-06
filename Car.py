import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from descartes import PolygonPatch


class Car:
    def __init__(self, car_speed, driver_level):
        # Car speed is equal to max car speed in km/h
        self.car_speed = car_speed
        # Driver level from 0 to 1 exmpl 0.58
        self.driver_level = driver_level

    def callculateActualSpeed(self):
        return self.car_speed * self.driver_level

    def ShowShortestPath(self, G, origin_p, destination_p, isPolice=False, multi=1):

        # Creating shortest path based on length
        route = nx.shortest_path(G, origin_p, destination_p, weight='length')
        # Plotting route
        if isPolice:
            fig, ax = ox.plot_graph_route(G, route, route_color='Blue', orig_dest_node_size=15 * multi, orig_dest_node_color="Blue",
                                          orig_dest_point_color="Blue")
        else:
            fig, ax = ox.plot_graph_route(G, route, route_color='Red', orig_dest_node_size=15 * multi, orig_dest_node_color="Red",
                                          orig_dest_point_color="Red")

    def returnRoute(self, G, origin_p, destination_p):
        # Creating shortest path based on length
        route = nx.shortest_path(G, origin_p, destination_p, weight='length')
        return route

    def calculatePathTime(self, G, route, origin_p,):

        # Creating list and adding zero indez\x
        route_times = [0]
        for n in range(1, len(route)):
            route_times.append((nx.shortest_path_length(
                G, origin_p, route[n], weight='length') / 1000) * 60 / 5)
        return route_times

    def pathTime(self, G, origin_p, destination_p):
        return nx.shortest_path_length(G, origin_p, destination_p, weight='length') / 1000 * 60 / 5
