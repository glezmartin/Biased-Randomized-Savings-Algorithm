"""
This module contains the function to generate positions in an array/list with biased random functions.
"""

import numpy as np
from types import FunctionType


def get_random_position(n: int, rand_function: FunctionType) -> int:
    """
    Returns a random position in a range given a distribution probability function

    Parameters
    ----------
    n : int
        length of the array
    rand_function : function
        the function that models how the distribution probability is constructed

    Returns
    -------
    position : int
        position selected in the array
    """
    position = 0
    while position < 0.5:
        position = int(np.round(rand_function(n)))
    return position - 1
