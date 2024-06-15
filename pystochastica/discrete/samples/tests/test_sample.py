from .. import Sample
import sympy as sp

X, Y, Z = sp.symbols('X, Y, Z')

def test_sample_arithmetic():
    sample1 = Sample(name=X, value=15)
    sample2 = Sample(name=Y, value=-5)
    sample3 = Sample(name=Z, value=3.5)

    assert (sample1 + sample2).name == X + Y
    assert (sample1 + sample2).value == 10

    assert (sample2*sample3).name == Y*Z
    assert (sample2*sample3).value == -17.5

    assert (sample1 - sample2 + sample3).name == X - Y + Z 
    assert (sample1 - sample2 + sample3).value == 23.5

    assert ((sample1 - sample2)*sample3).name == (X - Y)*Z
    assert ((sample1 - sample2)*sample3).value == 70

    assert (sample2**2).name == Y**2
    assert (sample2**2).value == 25

    assert (sample1 - sample1).name == 0
    assert (sample1 - sample1).value == 0

    assert (sample1 + 100).name == X + 100
    assert (sample1 + 100).value == 115

    assert (-1 - sample2 + 100).name == 99 - Y
    assert (-1 - sample2 + 100).value == 104