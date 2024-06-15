from ...samples import Sample
from ...variables import RandVar
from ...utils import generate_jdist_random, generate_jdist
from .. import RandVec
from decimal import Decimal
from fractions import Fraction
import sympy as sp
import numpy as np

X1, X2 = sp.symbols('X1, X2')
Y1, Y2 = sp.symbols('Y1, Y2')

jd_X1_X2_dict: dict = {
    (Sample(name=X1, value=1.5), Sample(name=X2, value=0)): 0.14,
    (Sample(name=X1, value=1.5), Sample(name=X2, value=1)): 0.35,
    (Sample(name=X1, value=-1), Sample(name=X2, value=0)): 0.19,
    (Sample(name=X1, value=-1), Sample(name=X2, value=1)): 0.32
}
jd_Y1_Y2_dict: dict = {
    (Sample(name=Y1, value=1.5), Sample(name=Y2, value=0)): 0.14,
    (Sample(name=Y1, value=1.5), Sample(name=Y2, value=1)): 0.35,
    (Sample(name=Y1, value=-1), Sample(name=Y2, value=0)): 0.19,
    (Sample(name=Y1, value=-1), Sample(name=Y2, value=1)): 0.32
}

def test_randrvec():
    rand_pspace = generate_jdist_random(dimension=5)
    Xrvec = RandVec(pspace=rand_pspace)
    assert Xrvec.dimension == len(Xrvec.components)

def test_rvec_moments():
    x1, x2 = sp.symbols('x1, x2')
    X1_dict = {'name': x1, 'pspace': {
            Sample(name=x1, value=-1): 0.34,
            Sample(name=x1, value=1): 0.66
        }}
    varX1 = RandVar(**X1_dict)
    varX1.calculate_expectation()

    X2_dict = {'name': x2, 'pspace': {
            Sample(name=x2, value=-1): 0.14,
            Sample(name=x2, value=1): 0.26,
            Sample(name=x2, value=0): 0.6
        }}
    varX2 = RandVar(**X2_dict)
    varX2.calculate_expectation()

    jdist = generate_jdist(varX1, varX2) # joint dist assumes varX1 and varX2 are independent
    X1_X2_rvec = RandVec(pspace=jdist)
    X1_X2_rvec.calculate_expectation()
    X1_X2_rvec.calculate_variance()
    print(X1_X2_rvec.cov_mtrx)
    sf = 5
    expectation_vec = [varX1.expectation, varX2.expectation]
    expectation_vec_shorthand = X1_X2_rvec.E
    assert all(
        round(X1_X2_rvec.expectation[i], sf) == round(expectation_vec[i], sf) for i in range(2))
    assert all(
        round(X1_X2_rvec.expectation[i], sf) == round(expectation_vec_shorthand[i], sf) for i in range(2))
    assert X1_X2_rvec.cov_mtrx.shape == (X1_X2_rvec.dimension, X1_X2_rvec.dimension)
    assert X1_X2_rvec.V.shape == (X1_X2_rvec.dimension, X1_X2_rvec.dimension)

def test_randvec_arithmetic():
    
    Xrvec = RandVec(pspace=jd_X1_X2_dict)
    Yrvec = RandVec(pspace=jd_Y1_Y2_dict)

    X_expectation = []
    for comp in Xrvec.components:
        comp.calculate_expectation()
        X_expectation += [comp.expectation]
    Y_expectation = []
    for comp in Yrvec.components:
        comp.calculate_expectation()
        Y_expectation += [comp.expectation]

    rvec_sum = Xrvec + Yrvec + [1.5, 1.5]
    rvec_sum.calculate_expectation()
    sf: int = 5
    assert rvec_sum.dimension == 2
    assert all(round(rvec_sum.expectation[i], sf) == round(X_expectation[i] + Y_expectation[i] + 1.5, sf) for i in range(rvec_sum.dimension))

def test_randvec_dot():

    rvec = RandVec(pspace=jd_X1_X2_dict)
    rvar = rvec.dot([1, 1])
    rvar.calculate_expectation()

    rvec_sum = rvec.sum()
    rvec_sum.calculate_expectation()
    print(rvec_sum.expectation)

    sf: int = 5
    assert isinstance(rvar, RandVar)
    assert isinstance(rvec_sum, RandVar)
    assert round(rvar.expectation, sf) == round(rvec_sum.expectation, sf)

def test_randvec_matmul():
    """testing matmul method on RandVec"""
    rvec = RandVec(pspace=jd_X1_X2_dict)
    rvec2 = RandVec(pspace=jd_Y1_Y2_dict)

    # __matmul__ and __rmatmul__
    rvec3 = rvec@rvec2
    rrvec3 = rvec2@rvec

    # __matmul__ and sum
    rvec_matmul_sum = rvec@[1, 1]
    rvec_matmul_sum.calculate_expectation()
    rvec_matmul_sum.calculate_variance()
    rvec_sum = rvec.sum()
    rvec_sum.calculate_expectation()
    rvec_sum.calculate_variance()

    sf: int = 5
    assert isinstance(rvec3, RandVar)
    assert rvec3 == rrvec3
    assert round(rvec_matmul_sum.expectation, sf) == round(rvec_sum.expectation, sf)
    assert round(rvec_matmul_sum.variance, sf) == round(rvec_sum.variance, sf)

def test_depsum():
    X = sp.Symbol('X')
    jd_XX = {
        (Sample(name=X, value=-1), Sample(name=X, value=1)): 0.0,
        (Sample(name=X, value=1), Sample(name=X, value=1)): 0.5,
        (Sample(name=X, value=-1), Sample(name=X, value=-1)): 0.5,
        (Sample(name=X, value=1), Sample(name=X, value=-1)): 0.0,
        }
    rvec = RandVec(pspace=jd_XX)
    rv = rvec@[1, -1]
    zero_rv = RandVar(name=sp.S.Zero, pspace={Sample(name=sp.S.Zero, value=0): 1.0})
    assert rv == zero_rv

def test_randvec_jd_randjd():
    random_randvec = RandVec(pspace=generate_jdist_random(dimension=5))
    sf = 5
    print(np.around(random_randvec.V, sf))
    assert random_randvec.V.shape == (random_randvec.dimension, random_randvec.dimension)
    assert all(random_randvec.V[i, i] > 0 for i in range(random_randvec.dimension)) # Cov(X, Y) < 0 only if X != Y; Cov(X, X) = Var(X) >= 0

def test_randvec_prob():
    
    rvec = RandVec(pspace=jd_X1_X2_dict)
    print(rvec.Prob('<=1.0'))
    print(rvec.Prob(['<=1.0', '==1.0']))
    assert isinstance(rvec.Prob('<=1.0'), (float, Decimal, Fraction))
    assert rvec.Prob('<=1.0') >= rvec.Prob(['<=1.0', '>=1.0'])
