"""
random variables and random vectors call on JointDistribution to evaluate probabilities
"""
from ._randvar_base import RandVarBase
from ._sample_base import SampleBase
import sympy as sp

class JointDistribution:

    def __new__(cls, *randvars, **joint_pspace):
        """
        for randvars pass RandVar or RandVarBase objects, (X, Y, ...)
        for joint_pspace pass dict {(X.sample, Y.sample, ...): prob}
        """
        # validation, each randvar in randvars is a RandVarBase object
        if not all(isinstance(rv, RandVarBase) for rv in randvars):
            raise TypeError(f"not all random variables are type {RandVarBase.__name__} objects")

        # validate joint_pspace keys 
        for sample_tuple in joint_pspace.keys():
            if not all(isinstance(sample, SampleBase) for sample in sample_tuple):
                raise TypeError(f"joint_dist keys are not all of type {SampleBase.__name__}")
            
            for i, sample in enumerate(sample_tuple):
                if not sample.name == randvars[i]:
                    raise NameError(f"name mismatch, got {sample.name} but expected {randvars[i].name}")
                
        # validate joint_pspace probabilities
        sf: int = max([rv.SIGFIGS for rv in randvars])
        probabilities_sum: float = sum(joint_pspace.values())
        if not round(probabilities_sum, sf) == 1.0:
            raise ValueError(f"total law of probability violated, got {probabilities_sum} but expected {1.0}")

        return super(JointDistribution, cls).__new__(cls)

    def __init__(self, *randvars , **joint_pspace) -> None:
        
        self.name: tuple[sp.Expr] = tuple([rv.name for rv in randvars])
        self.pspace: dict = joint_pspace

    def __str__(self) -> str:
        pass

    def __eq__(self, second_joint_dist: object) -> bool:
        pass 

    def __hash__(self) -> int:
        pass
