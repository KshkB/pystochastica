from .. import RandVar
from ...samples import Sample
import sympy as sp
import pytest

rv = 0
for i in range(15):
    name = sp.Symbol(f'x_{i}')
    rv += RandVar(
        name=name, 
        pspace={
            Sample(name=name, value=-1): 0.5,
            Sample(name=name, value=1): 0.5
        })

@pytest.fixture(scope='function')
def test_rv_pdf():
    rv.pdf(iterations=500)
    assert True

@pytest.fixture(scope='function')
def test_rv_cdf():
    rv.cdf()
    assert True