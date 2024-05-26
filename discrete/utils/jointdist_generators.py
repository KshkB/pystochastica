from ..core import SampleBase
from itertools import product
from  functools import reduce
from decimal import Decimal
from fractions import Fraction
import numpy as np
import sympy as sp

def list_product(array: list):
    return reduce(lambda x, y: x*y, array)

def generate_jdist(*marginals) -> dict:
    """
    from list of marginals, passed as list[RandVar], generate kwargs for joint distribution
        - joint distribution generated has marginals as its marginal distributions
        - Note, this joint distribution assumes marginals are independent
    """
    sample_prob_pairs_list = []
    for mg_rv in marginals:
        sample_prob_pairs = [(sample, Decimal(str(prob))) for sample, prob in mg_rv.pspace.items()]
        sample_prob_pairs_list += [sample_prob_pairs]

    sample_prob_pairs_all = product(*sample_prob_pairs_list)
    jd_pspace: dict = {}
    for sample_prob_pair in sample_prob_pairs_all:
        stacked = np.vstack(sample_prob_pair)
        jd_key = tuple(stacked[:,0])
        jd_value = list_product(stacked[:,1])
        try:
            jd_pspace[jd_key] += jd_value
        except KeyError:
            jd_pspace[jd_key] = jd_value

    return jd_pspace

def generate_jdist_random(\
        dimension: int = 3, 
        SAMPLE_SIZE_RANGE: tuple = (2, 6), 
        SAMPLE_VALUES: tuple = (-50, 50), 
        MIN: int = 1, 
        MAX: int = 100
        ) -> dict:
    """
    generate kwargs for dimension-dimensional joint distribution 
        - sample names are (X_0, X_1, ... X_{dimension-1}), default = 3
        - sample size range = number of samples for each random variable, SAMPLE_SIZE_RANGE, default = (1, 5)
        - sample values randomised between (SAMPLES_MIN, SAMPLES_MAX), default = (-50, 50)
        - joint probabilities randomised, generator seeded from (MIN, MAX), default range = (1, 100)
    returns a JointDistribution object
    """
    sample_names: list = [sp.Symbol(f"X_{i}") for i in range(dimension)]
    samples: dict = {sample_name: [] for sample_name in sample_names}
    for sample_name in sample_names:
        num_samples: int = np.random.randint(*SAMPLE_SIZE_RANGE)
        for _ in range(num_samples):
            value = Decimal(str(np.random.uniform(*SAMPLE_VALUES)))
            sample_object = SampleBase(name=sample_name, value=value)
            samples[sample_name] += [sample_object]

    jd_samples: list = list(product(*list(samples.values())))
    jd_sample_size: int = len(jd_samples)
    probabilities_pre = [np.random.randint(MIN, MAX) for _ in range(jd_sample_size)]
    probabilities = [Fraction(pre, sum(probabilities_pre)) for pre in probabilities_pre]
    return dict(zip(jd_samples, probabilities))
