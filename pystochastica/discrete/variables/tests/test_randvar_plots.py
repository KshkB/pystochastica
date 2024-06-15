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

# @pytest.fixture(scope='function')
def test_rv_pdf():
    rv.pdf(iterations=500, plt_kwargs = {'color': 'g', 'width': 0.5}, plt_methods = {'set_xticklabels': {'rotation': 45}})
    assert True

# @pytest.fixture(scope='function')
def test_rv_cdf():
    rv.cdf(plt_kwargs = {'color': 'y'}, plt_methods = {'set_xticklabels': {'rotation': 45}})
    assert True