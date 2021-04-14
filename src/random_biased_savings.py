"""
This module contains the functions to perform random biased savings algorithms with different functions
"""

import numpy as np
from types import FunctionType
import savings_algorithm
from _graph import Solution
from _biased_random_theorical_distribution import get_random_position


def rand_biased_savings(instance_name: str, rand_function: FunctionType) -> Solution:
    """
    Performs a random biased savings algorithm given an instance and the theoretical distribution function
    of the desired biased effect to apply to the algorithm

    Parameters
    ----------
    instance_name : str
        identifier of the instance
    rand_function : function
        the function that models how the distribution probability is constructed

    Returns
    -------
    solution : Solution
        the solution achieved by the random biased savings algorithm
    """

    # Algorithm initialization
    depot, nodes, veh_capacity = savings_algorithm.read_nodes(instance_name)
    savings_algorithm.build_initial_edges(depot, nodes)
    savings_list = savings_algorithm.compute_savings_list(nodes)
    solution = savings_algorithm.create_dummy_solution(nodes)

    # Algorithm iteration process of merging routes
    while len(savings_list) > 0:
        n = len(savings_list) - 1
        position = get_random_position(n, rand_function)
        candidate = savings_list[position]
        savings_algorithm.merge_routes(candidate, solution, depot, veh_capacity)
        savings_list.remove(savings_list[position])
    return solution


def iter_biased_savings(instance_name: str, iterations: int, rand_function: FunctionType) -> Solution:
    """
    Performs multiple iterations of a metaheuristic version of savings algorithm.
    As the metaheuristic version is not deterministic is a good practise to perform multiple iterations.

    Parameters
    ----------
    instance_name : str
        identifier of the instance
    iterations : int
        number of replicas of the metaheuristic search
    rand_function :
        the function that models how the distribution probability is constructed

    Returns
    -------
    best : Solution
        the solution with the lowest cost in the set of replicas
    """
    best = None
    for i in range(iterations):
        solution = rand_biased_savings(instance_name, rand_function)
        cost = solution.cost
        try:
            if cost < best.cost:
                best = solution
        except:
            best = solution
    return best


def triangular_rand_biased_savings(instance_name: str) -> Solution:
    """
    Performs a random biased savings algorithm with triangular distribution

    Parameters
    ----------
    instance_name : str
        identifier of the instance

    Returns
    -------
    solution : Solution
        the solution achieved by the random biased savings algorithm
    """
    rand_function = lambda n: (n + 1) * (1 - np.sqrt(np.random.random()))
    solution = rand_biased_savings(instance_name, rand_function)
    return solution


def geometrical_rand_biased_savings(instance_name: str, beta: float) -> Solution:
    """
    Performs a random biased savings algorithm with geometrical distribution

    Parameters
    ----------
    instance_name : str
        identifier of the instance
    beta : float
        parameter that models the uniformity of the distribution

    Returns
    -------
    solution : Solution
        the solution achieved by the random biased savings algorithm

    """
    rand_function = lambda n: (np.log(np.random.random()) / np.log(1 - beta)) % (n + 1)
    solution = rand_biased_savings(instance_name, rand_function)
    return solution


def iter_triangular_rand_biased_savings(instance_name: str, iterations: int) -> Solution:
    """
    Performs multiple iterations of triangular random biased savings algorithm
    and returns the solution with the lowest cost

    Parameters
    ----------
    instance_name : str
        identifier of the instance
    iterations : int
        number of replicas to perform

    Returns
    -------
    best : Solution
        the solution with the lowest cost in the set of replicas
    """
    rand_function = lambda n: (n + 1) * (1 - np.sqrt(np.random.random()))
    best = iter_biased_savings(instance_name, iterations, rand_function)
    return best


def iter_geometrical_rand_biased_savings(instance_name: str, beta: float, iterations: int) -> Solution:
    """
    Performs multiple iterations of geometrical random biased savings algorithm
    and returns the solution with the lowest cost

    Parameters
    ----------
    instance_name : str
        identifier of the instance
    iterations : int
        number of iterations to perform
    beta : float
        parameter that models the uniformity of the distribution

    Returns
    -------
    best : Solution
        the solution with the lowest cost in the set of replicas
    """
    rand_function = lambda n: (np.log(np.random.random()) / np.log(1 - beta)) % (n + 1)
    best = iter_biased_savings(instance_name, iterations, rand_function)
    return best
