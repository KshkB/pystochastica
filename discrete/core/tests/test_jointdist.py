from .. import SampleBase, JointDistribution
import sympy as sp

X, Y = sp.symbols('X, Y')

jd_init_dict: dict = {
    (SampleBase(name=X, value=1.5), SampleBase(name=Y, value=0)): 0.14,
    (SampleBase(name=X, value=1.5), SampleBase(name=Y, value=1)): 0.35,
    (SampleBase(name=X, value=-1), SampleBase(name=Y, value=0)): 0.19,
    (SampleBase(name=X, value=-1), SampleBase(name=Y, value=1)): 0.32
}

def test_jd_init():
    jd = JointDistribution(pspace=jd_init_dict)
    print(jd)
    assert jd.dimension == 2
    
def test_jd_marginals():
    jd = JointDistribution(pspace=jd_init_dict)
    jd.derive_marginals()
    for mg_var in jd.marginals:
        print(mg_var)
    assert len(jd.marginals) == jd.dimension

def test_jd_secondaries():
    jd = JointDistribution(pspace=jd_init_dict)
    jd.derive_secondaries()
    assert len(jd.secondaries) == 1

def test_jd_shorthands():
    jd = JointDistribution(pspace=jd_init_dict)
    for sc in jd.secnds:
        print(sc)
    assert len(jd.margs) == jd.dimension
    assert len(jd.secnds) == 1

