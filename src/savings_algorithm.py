"""
This module contains the necessary functions to implement the Clarke and Wright savings algorithm
"""

import csv
import operator
from itertools import combinations
from _graph import Node, Edge, Route, Solution


def _map_veh_capacity(instance_name: str) -> int:
    """
    Returns the vehicle capacity of a given instance

    Parameters
    ----------
    instance_name : str
        identifier of the instance
    Returns
    -------
    veh_capacity : int
        max amount of goods a vehicle can carry
    """
    with open('../data/veh_capacity.txt') as file:
        reader = csv.reader(file)
        capacities_dict = {row[0] : int(row[1]) for row in reader}
    veh_capacity = capacities_dict[instance_name]
    return veh_capacity


def read_nodes(instance_name: str) -> tuple:
    """
    Obtains the data needed to perform the savings algorithm over an instance

    Parameters
    ----------
    instance_name : str
        identifier of the instance to read

    Returns
    -------
    depot : Node
        the node from where the routes start
    nodes : Node
        the nodes to be supplied
    veh_capacity : int
        max amount of goods a vehicle can carry
    """
    veh_capacity = _map_veh_capacity(instance_name)
    file_name = '../data/{}_input_nodes.txt'.format(instance_name)
    with open(file_name) as instance:
        i = 0
        nodes = list()
        for line in instance:
            data = [float(x) for x in line.split()]
            i_node = Node(i, data[0], data[1], data[2])
            nodes.append(i_node)
            i += 1
    depot, nodes = nodes[0], nodes[1:]
    return depot, nodes, veh_capacity


def build_initial_edges(depot: Node, nodes: list) -> None:
    """
    Builds the edges of the dummy solution. This edges connect each node with the depot.
    This creates simple routes depot-node-depot for each node.

    Parameters
    ----------
    depot : Node
        the node from where the routes start
    nodes : Node
        the nodes to be supplied
    """
    for node in nodes:
        dn_edge = Edge(depot, node)
        nd_edge = dn_edge.reverse()
        node.dnEdge, node.ndEdge = dn_edge, nd_edge


def compute_savings_list(nodes: list) -> list:
    """
    Computes the savings list of Clarke and Wright savings algorithm

    Parameters
    ----------
    nodes : list
        the nodes to be supplied

    Returns
    -------
    savings_list : list
        ordered list with best candidates to save distance when merging routes
    """
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


def create_dummy_solution(nodes: list) -> Solution:
    """"
    Creates the initial solution. The initial solution consists in a set of dummy edges
    where exits as many routes as nodes. Each route consists in two edges depot-node and node-depot.

    Parameters
    ----------
    nodes : list
        the nodes to be supplied

    Returns
    -------
    solution : Solution
        initial dummy solution
    """
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


def _is_joinable(i_node: Node, j_node: Node, veh_capacity: int) -> bool:
    """
    Checks if two routes can be merged by a specific pair of nodes
    Two routes can be merged by two nodes if:
        - Both nodes are not interior
        - AND the nodes do not belong to the same route
        - AND the sum of the demand of both routes is not greater than the vehicle capacity

    Parameters
    ----------
    i_node : Node
        node to merge
    j_node : Node
        node to merge
    veh_capacity : int
        max amount of goods a vehicle can carry

    Returns
    -------
    bool
        specifies if it is possible to join both routes
    """
    condition1 = i_node.inRoute == j_node.inRoute
    condition2 = i_node.isInterior or j_node.isInterior
    condition3 = i_node.inRoute.demand + j_node.inRoute.demand > veh_capacity

    if condition1 or condition2 or condition3:
        return False
    else:
        return True


def _get_depot_edge(i_node: Node, depot: Node) -> Edge:
    """
    Returns the edge that connects the depot with the point desired to merge
    the points are able to merge so they must be exterior so the have to be connected to the depot
    there are only two options is the first stop in the route so the edge will be (depot, node)
    or is the last stop in the route so the edge will be (node, depot)
    could be both if a node is in it's initial status

    Parameters
    ----------
    i_node : Node
        a node to be supplied
    depot : Node
        the node from where the routes start

    Returns
    -------
    first_edge OR last_edge : Edge
        the edge that connects the node to the depot node
    """

    first_edge = i_node.inRoute.edges[0]
    last_edge = i_node.inRoute.edges[-1]

    if first_edge.origin == depot and first_edge.end == i_node:  # first edge
        return first_edge

    elif last_edge.origin == i_node and last_edge.end == depot:  # last edge
        return last_edge


def merge_routes(candidate: Edge, solution: Solution, depot: Node, veh_capacity: int) -> None:
    """
    Merges two routes if possible

    Parameters
    ----------
    candidate : Edge
        edge candidate to construct from the savings list
    solution : Solution
        solution that is being constructed
    depot: Node
        the node from where the routes start
    veh_capacity : int
        max amount of goods a vehicle can carry
    """

    # obtains the nodes where the union will be performed and checks if it is possible
    i_node, j_node = candidate.origin, candidate.end
    merge_test = _is_joinable(i_node, j_node, veh_capacity)

    # if possible makes the merge
    if merge_test is True:
        i_edge = _get_depot_edge(i_node, depot)
        j_edge = _get_depot_edge(j_node, depot)

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


def cw_savings(instance_name: str) -> Solution:
    """
    Computes the solution with the savings algorithm.

    Parameters
    ----------
    instance_name : str
        identifier of the instance
    Returns
    -------
    solution : Solution
        the solution achieved by the savings algorithm
    """
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
