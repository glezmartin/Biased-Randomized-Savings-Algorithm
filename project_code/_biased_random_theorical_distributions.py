"""
This file contains functions to generate positions in an array/list with biased random functions.
"""

import numpy as np


def get_random_triangular_position(n):
    """
    Returns the position in an array structure based on
    a biased random triangular distribution.
    
    Parameters
    ----------
    n : int
        Length of the array on which you want to obtain an index
    Returns
    -------
    position : int
        Position in the array 
    """
    position = 0
    while position < 0.5:
        position = (n+1) * (1 - np.sqrt(np.random.random())) 
    return int(np.round(position)) - 1


def get_random_geometric_position(n, beta):
    """
    Returns the position in an array structure based on
    a biased random geometric distribution.
    
    Parameters
    ----------
    n : int
        Length of the array on which you want to obtain an index
    beta : float
        Parameter that models the behavior of the distribution.
        When beta tends to zero, the more the distribution tends to uniformity.
    Returns
    -------
    position : int
        Position in the array
    """
    position = 0
    while position < 0.5:
        position = np.log(np.random.random()) / np.log(1 - beta)
        position = position % (n + 1)
        
    return int(np.round(position)) - 1
