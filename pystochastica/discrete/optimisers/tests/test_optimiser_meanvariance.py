from .. import MeanVariance
from ...vectors import RandVec
from ...utils import generate_jdist_random

def test_mvoptimiser():
    rvec: RandVec = RandVec(pspace=generate_jdist_random(dimension=5))
    expectation: float = sum(rvec.E)/rvec.dimension

    mv_optimiser = MeanVariance(rvec, expectation)
    mv_optimiser.optimise()
    print(f"{mv_optimiser.success}\n{mv_optimiser.message}\n{mv_optimiser.solution}")

    assert len(mv_optimiser.solution) == rvec.dimension
