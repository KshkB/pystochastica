from .. import SampleBase, RandVarBase
import sympy as sp 

name = sp.Symbol('X')
pspace: dict = {
    SampleBase(name=name, value=1.0): 0.34,
    SampleBase(name=name, value=-1): 0.66
}

def test_randvar_init():
    rv = RandVarBase(**{'name': name, 'pspace': pspace})
    print(rv)
    assert rv.name == name 

def test_randvar_eq():
    rv = RandVarBase(**{'name': name, 'pspace': pspace})
    rv2 = RandVarBase(**{'name': name, 'pspace': pspace})

    new_name = sp.Symbol('Y')
    new_pspace: dict = {    
        SampleBase(name=new_name, value=1.0): 0.34,
        SampleBase(name=new_name, value=-1): 0.66
        }
    rv3 = RandVarBase(**{'name': new_name, 'pspace': new_pspace})

    assert rv == rv2
    assert rv != rv3