from ...variables import RandVar
from ...core import JointDistribution
from .. import rvdict_to_pspace, generate_jdist, generate_jdist_random
import sympy as sp

X, Y, Z = sp.symbols('X, Y, Z')

X_dict: dict = {'name': X, 'pspace': {'-1': 0.5, '1': 0.5}}
Y_dict: dict = {'name': Y, 'pspace': {'-3': 0.15, '-2': 0.3, '0': 0.25, '2': 0.19, '3': 0.11}}
Z_dict: dict = {'name': Z, 'pspace': {'-0.5': 0.44, '0.4': 0.56}}

def test_jdist_generator():
    mX = RandVar(name=X, pspace=rvdict_to_pspace(X_dict))
    mY = RandVar(name=Y, pspace=rvdict_to_pspace(Y_dict))
    mZ = RandVar(name=Z, pspace=rvdict_to_pspace(Z_dict))
    marginals = [mX, mY, mZ]

    jd_kwargs = generate_jdist(*marginals)
    jd: JointDistribution = JointDistribution(pspace=jd_kwargs)
    jd.derive_marginals()
    jd_marginals = jd.marginals

    assert jd.dimension == 3
    assert all(jd_marginals[i] == marginals[i] for i in range(jd.dimension)) # marginals from jdist generated coincide with marginals passed

def test_jdist_random_gen():
    jd: JointDistribution = JointDistribution(pspace=generate_jdist_random(dimension=5))
    assert jd.dimension == 5
