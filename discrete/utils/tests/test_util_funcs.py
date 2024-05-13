from .. import *
from ...samples import Sample
import numpy as np
import sympy as sp

def test_convolve_dicts():
    
    nums1 = [0.1, 0.2, 0.55, 0.15]
    nums1_dict = dict(zip([i for i in range(len(nums1))], nums1))

    nums2 = [0.34, 0.66]
    nums2_dict = dict(zip([i for i in range(len(nums2))], nums2))

    np_convolved = np.convolve(nums1, nums2)
    dict_convolved = convolve_dicts(nums1_dict, nums2_dict)
    dict_convolved_arr = np.array(list(dict_convolved.values()))

    sf = 8
    assert all(np_convolved[i] == np.array(dict_convolved_arr)[i] for i in range(len(np_convolved)))
    assert round(sum(dict_convolved_arr), sf) == 1

dict1: dict = {2: 0.2, 3: 0.7, -2: 0.1}
dict2: dict = {0.5: 1}
dict3: dict= {-1: 0.15, 0: 0.24, 1: 0.43, 2: 0.18}
sf: int = 8

def test_convolve_dicts_many():
    
    convolved = convolve_dicts_many(dict1, dict2, dict3)
    assert round(sum(convolved.values()), sf) == 1

def test_dict_mul():

    multiplied = dict_mul(dict1, dict2, dict3)
    assert round(sum(multiplied.values()), sf) == 1

X = sp.Symbol('X')
rvX_dict: dict = {'name': X, 'pspace': {'-1': 0.5, '1': 0.5}}

def test_rv_to_sample():
    X_samples = rvdict_to_samples(rvX_dict)
    assert len(X_samples) == 2
    assert all(isinstance(sample, Sample) for sample in X_samples)

def test_rv_to_sample_to_rvdictinit():
    X_dictinit = rvdict_to_pspace(rvX_dict)
    sf = 8
    assert round(sum(X_dictinit.values()), sf) == 1

