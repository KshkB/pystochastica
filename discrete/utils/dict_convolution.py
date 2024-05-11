"""
numpy.convolve(array1, array2) is a dict convolution where keys are indices of the arrays
more generally, dict convolution is a convolution of values associated to arbitrary numbers
    - e.g., it is numpy.convolve if the indices can be arbitrary real numbers
"""
from itertools import product
import numpy as np

def depr_convolve_dicts(first_dict: dict, second_dict: dict) -> dict:
    """note, dict keys and values are (int, float) type"""
    convolved_dict: dict = {}
    for key, val in first_dict.items():
        for key2, val2 in second_dict.items():
            try:
                convolved_dict[key + key2] += val*val2 
            except KeyError:
                convolved_dict[key + key2] = val*val2
    return convolved_dict

def convolve_dicts(first_dict: dict, second_dict: dict) -> dict:
    """
    uses one explicit for-loop with an iterator.product object
    returns a dict representing the results of the convolution
    """
    key_value_pairs = product(first_dict.items(), second_dict.items())
    convolved: dict = {}
    for (k1, v1), (k2, v2) in key_value_pairs:
        try:
            convolved[k1 + k2] += v1*v2
        except KeyError:
            convolved[k1 + k2] = v1*v2

    return convolved

def convolve_dicts_many(*dicts) -> dict:
    """
    pass an arbitrary number of dicts of type {float: float}, return their convolution
    """
    key_value_pairs = product(*[d.items() for d in dicts])
    convolved: dict = {}
    for key_values in key_value_pairs:
        stacked = np.vstack(key_values)
        key = np.sum(stacked[:,0]) 
        value = np.prod(stacked[:,1])
        try:
            convolved[key] += value
        except KeyError:
            convolved[key] = value 

    return convolved

