# Biased Randomized Savings Algorithm
This repository studies the effect that different methods of biased random selection have on the savings algorithm (Clarke and Wright, 1964).

## Introduction

The vehicle routing problem (VRP) is a combinatorial optimization and integer programming problem which asks "What is the optimal set of routes for a fleet of vehicles to traverse in order to deliver to a given set of customers?". Determining the optimal solution to VRP is NP-hard. In 1964, Clarke and Wright improved on Dantzig and Ramser's approach using an effective greedy approach called the savings algorithm (“Vehicle routing problem,” 2020).

The aim of this project is to include in the route selection process of the savings algorithm a biased randomization algorithm. In this way we will avoid destroying the logic behind the heuristic but at the same time giving the opportunity to the algorithm to have a random component that can allow us to obtain better solutions than the initial deterministic algorithm.

## Table of contents
* [C&W Savings algorithm](https://github.com/glezmartin/Biased-Randomized-Savings-Algorithm/blob/main/project_code/_savings_algorithm.py)
* [Test of the benchmark examples of C&W Savings Algorithm](https://github.com/glezmartin/Biased-Randomized-Savings-Algorithm/blob/main/project_code/cw_savings_benchmark.ipynb)
* [Skewed Distributions](https://github.com/glezmartin/Biased-Randomized-Savings-Algorithm/blob/main/project_code/skewed_th_prob_distr.ipynb)
* [Biased-Randomizied Savings Algorithm](https://github.com/glezmartin/Biased-Randomized-Savings-Algorithm/blob/main/project_code/_random_biased_savings.py)
* [Test of the benchmark example of the modified C&W Savings Algorithm](https://github.com/glezmartin/Biased-Randomized-Savings-Algorithm/blob/main/project_code/rb_savings_benchmark.ipynb)

![Monte Carlo Simulation Solution](https://github.com/glezmartin/Biased-Randomized-Savings-Algorithm/blob/main/reports/figures/MCS_solution.png)
