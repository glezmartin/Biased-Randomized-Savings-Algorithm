"""
This script performs a test of the different theoretical distributions available to select routes
in the savings list generated by C&W savings algorithm
"""

import os
import pandas as pd
from savings_algorithm import cw_savings
from random_biased_savings import iter_geometrical_rand_biased_savings, iter_triangular_rand_biased_savings

# read the instances
instances = filter(lambda x: x.endswith('input_nodes.txt'), os.listdir('../data'))
instances = list(map(lambda x: x[: x.find('_')], instances))
instances.sort()

# set number of replicas to perform in the random biased search
replicas = 50
costs = dict()

for instance in instances:
    original_solution = cw_savings(instance)
    triangular_solution = iter_triangular_rand_biased_savings(instance, replicas)
    geometrical_solution_1 = iter_geometrical_rand_biased_savings(instance, 0.1, replicas)
    geometrical_solution_2 = iter_geometrical_rand_biased_savings(instance, 0.2, replicas)
    geometrical_solution_3 = iter_geometrical_rand_biased_savings(instance, 0.3, replicas)
    geometrical_solution_4 = iter_geometrical_rand_biased_savings(instance, 0.4, replicas)
    geometrical_solution_5 = iter_geometrical_rand_biased_savings(instance, 0.5, replicas)
    geometrical_solution_6 = iter_geometrical_rand_biased_savings(instance, 0.6, replicas)
    geometrical_solution_7 = iter_geometrical_rand_biased_savings(instance, 0.7, replicas)
    geometrical_solution_8 = iter_geometrical_rand_biased_savings(instance, 0.8, replicas)
    geometrical_solution_9 = iter_geometrical_rand_biased_savings(instance, 0.9, replicas)
    costs[instance] = {'original': original_solution.cost,
                       f'triangular n={replicas}' : triangular_solution.cost,
                       f'geometrical n={replicas}, beta=0.1' : geometrical_solution_1.cost,
                       f'geometrical n={replicas}, beta=0.2' : geometrical_solution_2.cost,
                       f'geometrical n={replicas}, beta=0.3' : geometrical_solution_3.cost,
                       f'geometrical n={replicas}, beta=0.4' : geometrical_solution_4.cost,
                       f'geometrical n={replicas}, beta=0.5' : geometrical_solution_5.cost,
                       f'geometrical n={replicas}, beta=0.6' : geometrical_solution_6.cost,
                       f'geometrical n={replicas}, beta=0.7' : geometrical_solution_7.cost,
                       f'geometrical n={replicas}, beta=0.8' : geometrical_solution_8.cost,
                       f'geometrical n={replicas}, beta=0.9' : geometrical_solution_9.cost}

results = pd.DataFrame(costs).T
#results.to_csv('../reports/datasets/theoretical_distributions_results.csv')
