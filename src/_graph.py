"""
This module contains the necessary classes to create a graph solution of Clarke and Wright savings algorithm
or any metaheuristic modification of it
"""

import math
import matplotlib.pyplot as plt
import networkx as nx


class Node:
    """
    A class to represent a node

    Attributes
    ----------
    ID : int
        node identifier
    x : int
        x-coordinate of the node
    y : int
        y-coordinate of the node
    demand : int
        demand of the node
    inRoute : Route
        route which the node belongs to
    isInterior : bool
        tells if the route is not connected to the depot node
    dnEdge : Edge
        edge that connects the depot node to the depot
    ndEdge : Edge
        edge that connects the node to the depot node

    Methods
    -------
    __repr__()
        establishes how the class is printed
    """
    def __init__(self, node_id, x, y, demand):
        """
        Parameters
        ----------
        node_id : int
            node identifier
        x : int
            x-coordinate of the node
        y : int
            y-coordinate of the node
        demand : int
            demand of the node
        """
        self.ID = node_id  # Node identifier
        self.x = x  # x-coordinate
        self.y = y  # y-coordinate
        self.demand = demand
        self.inRoute = None  # route to which the node belongs
        self.isInterior = False  # an interior node is not connected to depot
        self.dnEdge = None  # edge from depot to this node
        self.ndEdge = None  # edge from node to depot

    def __repr__(self):
        return 'Node {}'.format(self.ID)


class Edge:
    """
    A class to represent an Edge

    Parameters
    ----------
    origin : Node
        origin node of the edge
    end : Node
        end node of the edge

    Methods
    -------
    __repr__()
        establishes how the class is printed
    __abs__()
        calculates the Euclidean distance of the edge
    reverse()
        reverses the direction of the edge
    """
    def __init__(self, origin, end):
        """
        Parameters
        ----------
        origin : Node
            origin node of the edge
        end : Node
            end node of the edge
        """
        self.origin = origin  # origin node of the edge
        self.end = end  # end node of the edge
        self.cost = abs(self)
        self.savings = 0.0
        self.invEdge = None

    def __repr__(self):
        return 'Edge (Node {} -> Node {})'.format(self.origin.ID, self.end.ID)

    def __abs__(self):
        """
        Returns the Euclidean distance of the edge

        Returns
        -------
        distance : float
            distance between origin node and end node
        """
        distance = math.sqrt((self.origin.x - self.end.x) ** 2 + (self.origin.y - self.end.y) ** 2)
        return distance

    def reverse(self):
        """
        Returns the reversed edge by setting the origin of the reversed
        edge as the end node of the original edge and vice versa.

        Returns
        -------
        reversed_edge : Edge
            original edge with reversed origin and endpoint
        """
        reversed_edge = Edge(self.end, self.origin)
        return reversed_edge


class Route:
    """
    A class to represent a route

    Methods
    -------
    __repr__()
        establishes how to class is printed
    __iadd__(edge)
        appends to the route the edge passed and modifies the properties of it
    __isub__(edge)
        subtracts the edge passed and modifies the properties of it
    reverse()
        reverses the order of the edges in the route
    """
    def __init__(self):
        """
        Parameters
        ----------
        cost : float
            cost in distance of the route
        edges : list
            the set of edges that the route includes
        demand : float
            total demand covered by the route
        """
        self.cost = 0.0
        self.edges = []
        self.demand = 0.0

    def __repr__(self):
        return 'Route ({}{})'.format(''.join([f'{edge.origin.ID} -> ' for edge in self.edges]), self.edges[-1].end.ID)

    def __iadd__(self, edge):
        """
        Appends to the route the edge passed and modifies the properties of it

        Parameters
        ----------
        edge : Edge
            the edge to append to the route

        Returns
        -------
        self
        """

        self.cost += edge.cost
        self.demand += edge.end.demand
        self.edges.append(edge)
        return self

    def __isub__(self, edge):
        """
        Subtracts the edge passed and modifies the properties of it

        Parameters
        ----------
        edge : Edge
            the edge to delete from the route

        Returns
        -------
        self
        """
        self.cost -= edge.cost
        self.edges.remove(edge)
        return self

    def reverse(self):
        """
        Reverses the order of the edges in the route
        """
        self.edges = [edge.reverse() for edge in reversed(self.edges)]


class Solution:
    """
    A class to represent a solution graph as a set of feasible routes

    Attributes
    ----------
    ID : int
        solution identifier
    routes : list
        set of routes that the solution contains
    cost : float
        sum of the costs of each route that belongs to the solution
    demand : float
        sum of the demand of each route that belongs to the solution

    Methods
    -------
    __iadd__(edge)
        appends to the route the route passed and modifies the properties of the solution
    __isub__(edge)
        subtracts the route passed and modifies the properties of the solution
    plot_routes()
        plots a picture of the solution graph
    """
    last_ID = -1

    def __init__(self):
        Solution.last_ID += 1
        self.ID = Solution.last_ID
        self.routes = []
        self.cost = 0.0
        self.demand = 0.0

    def __iadd__(self, route):
        """
        Appends to the solution the route passed and modifies the properties of the solution

        Parameters
        ----------
        route : Route
            the route to append to the solution
        Returns
        -------
        self
        """
        self.cost += route.cost
        self.demand += route.demand
        self.routes.append(route)
        return self

    def __isub__(self, route):
        """
        Subtracts from the solution the route passed and modifies the properties of the solution

        Parameters
        ----------
        route : Route
            the route to subtract from the solution
        Returns
        -------
        self
        """
        self.cost -= route.cost
        self.demand -= route.demand
        self.routes.remove(route)
        return self

    def plot_routes(self):
        """
        Plots the solution graph
        """
        plt.figure(figsize=(20, 10))
        ax = plt.gca()
        g = nx.Graph()

        # Adds the edges to the Graph object
        for route in self.routes:
            for edge in route.edges:
                g.add_edge(edge.origin.ID, edge.end.ID)
                g.add_node(edge.end.ID, coord=(edge.end.x, edge.end.y))
        coord = nx.get_node_attributes(g, 'coord')

        # plots the graph using networkx
        nx.draw_networkx(g, coord, edge_color='#3B61AF', node_color='#1EC16B')

        # Modifies the aspect and sets the plot title
        plt.title('Cost = {}'.format(self.cost))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
