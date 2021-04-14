# Biased Randomized Savings Algorithm
This repository studies the effect that different methods of biased random selection have on the savings algorithm (Clarke and Wright, 1964).

## Introduction

The vehicle routing problem (VRP) is a combinatorial optimization and integer programming problem which asks "What is the optimal set of routes for a fleet of vehicles to traverse in order to deliver to a given set of customers?". Determining the optimal solution to VRP is NP-hard. In 1964, Clarke and Wright improved on Dantzig and Ramser's approach using an effective greedy approach called the savings algorithm (“Vehicle routing problem,” 2020).

The aim of this project is to include in the route selection process of the savings algorithm a biased randomization algorithm. In this way we will avoid destroying the logic behind the heuristic but at the same time giving the opportunity to the algorithm to have a random component that can allow us to obtain better solutions than the initial deterministic algorithm.

This project is part of the Metaheuristic Optimization course of the Master in Computational Engineering and Mathematics of the Universitat Rovira i Virgilli.

## Table of contents
* [C&W Savings algorithm](https://github.com/glezmartin/Biased-Randomized-Savings-Algorithm/blob/main/src/savings_algorithm.py)
* [C&W Savings algorithm example (Jupyter notebook)](https://github.com/glezmartin/Biased-Randomized-Savings-Algorithm/blob/main/notebooks/C%26W%20Savings%20Algorithm.ipynb)
* [Random biased alternatives](https://github.com/glezmartin/Biased-Randomized-Savings-Algorithm/blob/main/src/random_biased_savings.py)
* [Random biased alternatives example (Jupyter notebook)](https://github.com/glezmartin/Biased-Randomized-Savings-Algorithm/blob/main/notebooks/Random%20Biased%20Savings%20with%20Theoretical%20Distributions.ipynb)
* [Testing algorithms with theoretical distributions](https://github.com/glezmartin/Biased-Randomized-Savings-Algorithm/blob/main/notebooks/Testing%20algorithms%20with%20theoretical%20distributions.ipynb)


![](https://github.com/glezmartin/Biased-Randomized-Savings-Algorithm/blob/main/reports/figures/MCS_solution.png)
