from _biased_random_theorical_distributions import *
from _savings_algorithm import *
import numpy as np


def rand_biased_tri_savings(instance_name):
    depot, nodes, veh_capacity = read_nodes(instance_name)
    build_initial_edges(depot, nodes)
    savings_list = compute_savings_list(nodes)
    solution = create_dummy_solution(nodes)
    
    while len(savings_list) > 0:
        n = len(savings_list) - 1 
        position = get_random_triangular_position(n)
        candidate = savings_list[position]
        merge_routes(candidate, solution, depot, veh_capacity)
        savings_list.remove(savings_list[position])

    return solution


def test_triangular(instance_name, iterations):
    best = None
    for i in range(iterations):
        solution = rand_biased_tri_savings(instance_name)
        cost = solution.cost
        try:
            if cost < best.cost:
                best = solution
        except:
            best = solution
        # print('solution_{} --- cost = {}'.format(i, cost))
    return best


def rand_biased_geom_savings(instance_name,beta):
    depot, nodes, veh_capacity = read_nodes(instance_name)
    build_initial_edges(depot, nodes)
    savings_list = compute_savings_list(nodes)
    solution = create_dummy_solution(nodes)
    
    while len(savings_list) > 0:
        n = len(savings_list) - 1 
        position = get_random_geometric_position(n, beta)
        candidate = savings_list[position]
        merge_routes(candidate, solution, depot, veh_capacity)
        savings_list.remove(savings_list[position])

    return solution


def test_geometrical(instance_name, beta, iterations):
    best = None
    for i in range(iterations):
        solution = rand_biased_geom_savings(instance_name, beta)
        cost = solution.cost
        try:
            if cost < best.cost:
                best = solution
        except:
            best = solution
        # print('solution_{} --- cost = {}'.format(i, cost))
    return best


def test_random_geometrical(instance_name, low, high, iterations):
    low, high = low * 100, high * 100
    best = None
    for i in range(iterations):
        solution = rand_biased_geom_savings(instance_name, np.random.randint(low=low, high=high)/100)
        cost = solution.cost
        try:
            if cost < best.cost:
                best = solution
        except:
            best = solution
        # print('solution_{} --- cost = {}'.format(i, cost))
    return best