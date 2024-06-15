from .. import RandVar
from ...utils import rvdict_to_pspace
from decimal import Decimal
import sympy as sp

X, Y, Z = sp.symbols('X, Y, Z')

X_dict: dict = {'name': X, 'pspace': {'-1': 0.5, '1': 0.5}}
Y_dict: dict = {'name': Y, 'pspace': {'-3': 0.15, '-2': 0.3, '0': 0.25, '2': 0.19, '3': 0.11}}
Z_dict: dict = {'name': Z, 'pspace': {'-0.5': 0.44, '0.4': 0.56}}

def test_randvar_meanvar():

    X_pspace = rvdict_to_pspace(X_dict)
    
    rvX = RandVar(name=X, pspace=X_pspace)
    rvX.calculate_expectation()
    rvX.calculate_variance()
    assert rvX.expectation == 0
    assert rvX.variance == 1

def test_variance():

    X_pspace = rvdict_to_pspace(X_dict)

    X1 = RandVar(name=X, pspace=X_pspace)
    X1.calculate_expectation()
    X1.calculate_variance()

    X2_dict = {'name': Y, 'pspace': X_dict['pspace']}
    Y_pspace = rvdict_to_pspace(X2_dict)
    X2 = RandVar(name=Y, pspace=Y_pspace)
    X2.calculate_expectation()
    X2.calculate_variance()

    diff = X1 - X2 
    diff.calculate_expectation()
    diff.calculate_variance()
    print(f"{diff.variance = }")
    assert diff.expectation == 0
    assert not diff.variance == 0 # variance != 0 since X1 is indepdent of X2

def test_randvar_arithmetic():
    
    X_pspace = rvdict_to_pspace(X_dict)
    rvX = RandVar(name=X, pspace=X_pspace)
    rvX.calculate_expectation()
    rvX.calculate_variance()

    Y_pspace = rvdict_to_pspace(Y_dict)
    rvY = RandVar(name=Y, pspace=Y_pspace)
    rvY.calculate_expectation()
    rvY.calculate_variance()

    Z_pspace = rvdict_to_pspace(Z_dict)
    rvZ = RandVar(name=Z, pspace=Z_pspace)
    rvZ.calculate_expectation()
    rvZ.calculate_variance()

    rvU = rvX + rvY + rvZ 
    rvU.calculate_expectation()
    rvU.calculate_variance()

    rvV = -3.1*rvX*rvY*rvZ # __neg__, __mul__ and __rmul__
    rvV.calculate_expectation()
    rvV.calculate_variance()

    # test __pow__ and check variance against explicit formula
    rvX2 = rvX**2
    rvX2.calculate_expectation()
    rvY2 = rvY**2 
    rvY2.calculate_expectation()
    rvZ2 = rvZ**2
    rvZ2.calculate_expectation()

    rvZ3 = rvZ**3
    rvZ3.calculate_expectation()
    rvW  = 2*rvX**2 + 1.3*rvX*rvY - 0.2*rvZ**3 # polynomial variable
    rvW.calculate_expectation()

    sf: int = 8
    assert round(rvU.expectation, sf) == round(rvX.expectation + rvY.expectation + rvZ.expectation, sf)
    assert round(rvU.variance, sf) == round(rvX.variance + rvY.variance + rvZ.variance, sf) # since X, Y, Z are i.i.d.

    assert round(rvV.expectation, sf) == -3.1*rvX.expectation*rvY.expectation*rvZ.expectation
    assert round(rvV.variance, sf) == round(((-3.1)**2)*(rvX2.expectation*rvY2.expectation*rvZ2.expectation\
                                                 - (rvX.expectation*rvY.expectation*rvZ.expectation)**2), sf)

    assert round(rvW.expectation, sf) == round(2*rvX2.expectation + 1.3*rvX.expectation*rvY.expectation\
                                            - 0.2*rvZ3.expectation, sf)
    
def test_randvar_shorthand():

    X_pspace = rvdict_to_pspace(X_dict)
    rvX = RandVar(name=X, pspace=X_pspace)
    rvX.calculate_expectation()
    rvX.calculate_variance()

    sf: int = 5
    assert round(rvX.E, sf) == round(rvX.expectation, sf)
    assert round(rvX.V, sf) == round(rvX.variance, sf)

def test_randvar_prob():

    rvX = RandVar(name=X, pspace=rvdict_to_pspace(X_dict))
    rvY = RandVar(name=Y, pspace=rvdict_to_pspace(Y_dict))
    rvZ = RandVar(name=Z, pspace=rvdict_to_pspace(Z_dict))

    U = rvX + rvY + rvZ 
    sf = 5
    print(f"{U.Prob('<= 1') = :.{sf}f}")

    assert isinstance(U.Prob('<= 1'), (float, Decimal))

