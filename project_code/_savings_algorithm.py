import math
import operator
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations


def map_veh_capacity(instance_name):
    capacities = {'A-n32-k5': 100,
                  'A-n38-k5': 100,
                  'A-n45-k7': 100,
                  'A-n55-k9': 100,
                  'A-n60-k9': 100,
                  'A-n61-k9': 100,
                  'A-n65-k9': 100,
                  'A-n80-k10': 100,
                  'B-n50-k7': 100,
                  'B-n52-k7': 100,
                  'B-n57-k9': 100,
                  'B-n78-k10': 100,
                  'E-n22-k4': 6000,
                  'E-n30-k3': 4500,
                  'E-n33-k4': 8000,
                  'E-n51-k5': 160,
                  'E-n76-k10': 140,
                  'E-n76-k14': 100,
                  'E-n76-k7': 220,
                  'F-n135-k7': 2210,
                  'F-n45-k4': 2010,
                  'F-n72-k4': 30000,
                  'M-n101-k10': 200,
                  'M-n121-k7': 200,
                  'P-n101-k4': 400,
                  'P-n22-k8': 3000,
                  'P-n40-k5': 140,
                  'P-n50-k10': 100,
                  'P-n55-k15': 70,
                  'P-n65-k10': 130,
                  'P-n70-k10': 135,
                  'P-n76-k4': 350,
                  'P-n76-k5': 280}
    return capacities[instance_name]


def read_nodes(instance_name):
    veh_capacity = map_veh_capacity(instance_name)
    file_name = '../project_data/{}_input_nodes.txt'.format(instance_name)
    with open(file_name) as instance:
        i = 0
        nodes = list()
        for line in instance:
            data = [float(x) for x in line.split()]
            i_node = Node(i, data[0], data[1], data[2])
            nodes.append(i_node)
            i += 1
    return nodes[0], nodes[1:], veh_capacity


def build_initial_edges(depot, nodes):
    for node in nodes:
        dn_edge = Edge(depot, node)
        nd_edge = dn_edge.reverse()
        node.dnEdge, node.ndEdge = dn_edge, nd_edge


def compute_savings_list(nodes):
    savings_list = list()
    candidates_list = combinations(nodes, 2)
    for iNode, jNode in candidates_list:
        ij_edge = Edge(iNode, jNode)
        ji_edge = ij_edge.reverse()

        ij_edge.invEdge = ji_edge
        ji_edge.invEdge = ij_edge
        ij_edge.savings = iNode.ndEdge.cost + jNode.dnEdge.cost - ij_edge.cost
        ji_edge.savings = ij_edge.savings

        savings_list.append(ij_edge)
    savings_list.sort(key=operator.attrgetter('savings'), reverse=True)
    return savings_list


def create_dummy_solution(nodes):
    solution = Solution()
    for node in nodes:
        dn_edge = node.dnEdge
        nd_edge = node.ndEdge

        # Creates and modify the route
        dnd_route = Route()
        dnd_route += dn_edge
        dnd_route += nd_edge

        # Changes node parameters
        node.inRoute = dnd_route
        node.isInterior = False

        # Adds the route in the solution
        solution += dnd_route
    return solution


def check_merging_conditions(i_node, j_node, veh_capacity):
    # The combination of both is possible if:
    # The nodes are not interior
    # The nodes are not in the same route
    # The sum of the demand of both routes is not larger than the capacity of the vehicle
    if i_node.inRoute == j_node.inRoute:
        return False
    elif i_node.isInterior is True or j_node.isInterior is True:
        return False
    elif i_node.inRoute.demand + j_node.inRoute.demand > veh_capacity:
        return False
    else:
        return True


def get_depot_edge(i_node, depot):
    # Returns the edge that connects the depot with the point desired to merge
    # the points are able to merge so they must be exterior so the have to be connected to the depot
    # there are only two options is the first stop in the route so the edge will be (depot, node)
    # or is the last stop in the route so the edge will be (node, depot)
    # could be both if a node is in it's initial status

    first_edge = i_node.inRoute.edges[0]
    last_edge = i_node.inRoute.edges[-1]

    if first_edge.origin == depot and first_edge.end == i_node:  # first edge
        return first_edge

    elif last_edge.origin == i_node and last_edge.end == depot:  # last edge
        return last_edge


def merge_routes(candidate, solution, depot, veh_capacity):
    i_node, j_node = candidate.origin, candidate.end
    merge_test = check_merging_conditions(i_node, j_node, veh_capacity)

    if merge_test is True:
        i_edge = get_depot_edge(i_node, depot)
        j_edge = get_depot_edge(j_node, depot)

        i_route = i_node.inRoute
        j_route = j_node.inRoute
        solution -= j_route
        solution -= i_route

        i_route -= i_edge
        if i_edge.origin == depot:
            i_route.reverse()

        if len(i_route.edges) > 1:
            i_node.isInterior = True

        j_route -= j_edge
        if j_edge.end == depot:
            j_route.reverse()

        if len(j_route.edges) > 1:
            j_node.isInterior = True

        i_route += candidate
        j_node.inRoute = i_route

        for edge in j_route.edges:
            i_route += edge
            node = edge.end
            node.inRoute = i_route
        solution += i_route


def cw_savings(instance_name):
    # reads the data of the given instance
    depot, nodes, veh_capacity = read_nodes(instance_name)
    build_initial_edges(depot, nodes)
    # savings list construction
    savings_list = compute_savings_list(nodes)

    # creates the dummy solution where every node has its own route depot-node-depot
    solution = create_dummy_solution(nodes)

    # iterates over the savings list and merge every candidate that satisfies the conditions
    for candidate in savings_list:
        merge_routes(candidate, solution, depot, veh_capacity)

    return solution


class Node:
    def __init__(self, node_id, x, y, demand):
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
    def __init__(self, origin, end):
        self.origin = origin  # origin node of the edge
        self.end = end  # end node of the edge
        self.cost = abs(self)
        self.savings = 0.0
        self.invEdge = None

    def __repr__(self):
        return 'Edge (Node {} -> Node {})'.format(self.origin.ID, self.end.ID)

    def __abs__(self):  # calculates the Euclidean distance of the edge
        return math.sqrt((self.origin.x - self.end.x) ** 2 + (self.origin.y - self.end.y) ** 2)

    def reverse(self):
        return Edge(self.end, self.origin)


class Route:
    def __init__(self):
        self.cost = 0.0  # cost of this route
        self.edges = []  # sorted edges in this route
        self.demand = 0.0  # total demand covered by this route

    def __repr__(self):
        return 'Route ({}{})'.format(''.join([f'{edge.origin.ID} -> ' for edge in self.edges]), self.edges[-1].end.ID)

    def __iadd__(self, edge):
        # Appends to the route the edge passed and modifies the properties of it
        self.cost += edge.cost
        self.demand += edge.end.demand
        self.edges.append(edge)
        return self

    def __isub__(self, edge):
        # Subtracts the edge passed and modifies the properties of it
        self.cost -= edge.cost
        self.edges.remove(edge)
        return self

    def reverse(self):
        self.edges = [edge.reverse() for edge in reversed(self.edges)]


class Solution:
    last_ID = -1

    def __init__(self):
        Solution.last_ID += 1
        self.ID = Solution.last_ID
        self.routes = []
        self.cost = 0.0
        self.demand = 0.0

    def __iadd__(self, route):
        self.cost += route.cost
        self.demand += route.demand
        self.routes.append(route)
        return self

    def __isub__(self, route):
        self.cost -= route.cost
        self.demand -= route.demand
        self.routes.remove(route)
        return self

    def plot_routes(self):
        plt.figure(figsize=(20, 10))
        ax = plt.gca()
        g = nx.Graph()
        for route in self.routes:
            for edge in route.edges:
                g.add_edge(edge.origin.ID, edge.end.ID)
                g.add_node(edge.end.ID, coord=(edge.end.x, edge.end.y))
        coord = nx.get_node_attributes(g, 'coord')
        nx.draw_networkx(g, coord, edge_color='#3B61AF', node_color='#1EC16B')
        plt.title('Cost = {}'.format(self.cost))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
