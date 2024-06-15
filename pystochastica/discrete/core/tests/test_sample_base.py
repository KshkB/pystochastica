from .. import SampleBase
import sympy as sp

name = sp.Symbol('X')
value: float = 3.5

def test_sample_init():
    sample_obj = SampleBase(**{'name': name, 'value': value})
    print(sample_obj)
    assert sample_obj.value == 3.5

def test_sample_eq():
    sample_obj = SampleBase(**{'name': name, 'value': value})
    second_sample = SampleBase(**{'name': name, 'value': value})

    another_name = sp.Symbol('Y')
    another_value: float = 3
    third_sample = SampleBase(**{'name': another_name, 'value': another_value})

    assert sample_obj == second_sample
    assert not sample_obj == third_sample
