"""
multiply *dicts of type *{float: float}, return dict {float: float}
"""
from itertools import product
import numpy as np

def dict_mul(*dicts) -> dict:

    key_value_pairs = product(*[d.items() for d in dicts])
    multiplied: dict = {}
    for key_values in key_value_pairs:
        stacked = np.vstack(key_values)
        key = np.prod(stacked[:,0])
        prob = np.prod(stacked[:,1])

        try:
            multiplied[key] += prob 
        except KeyError:
            multiplied[key] = prob 
            
    return multiplied
