"""
random variables and random vectors call on JointDistribution to evaluate probabilities
"""
from ._sample_base import SampleBase
from ._randvar_base import RandVarBase
import numpy as np
class JointDistribution:

    SIGFIGS: int = 8 # default numerical accuracy for probabilities

    def __new__(cls, **kwargs):
        """
        pass dict {tuple[Sample]: float} 
            - e.g., {(sample1, sample2, ...): prob}
        
        Note. Random variables are marginals as derived from the joint distribution
        If random variables are passed individually, it means they are independent
            - independent variables are marginals of joint distributions if the joint distribution is the product distribution
            - i.e., if P(X, Y) = P(X)P(Y), which just means (X, Y) are independent
        """
        pspace: dict = kwargs['pspace']
        
        # validation of pspace keys, must be all of type Sample
        if not all(isinstance(sample, SampleBase) for sample_tuple in pspace.keys() for sample in sample_tuple):
            raise TypeError(f"not all samples in the probability space are of type {SampleBase.__name__}")
        
        # validation, each sample tuple must have the same length
        dimension = next(len(sample_tuple) for sample_tuple in pspace.keys())
        for sample_tuple in pspace.keys():
            if not len(sample_tuple) == dimension:
                raise ValueError(f"dimension mismatch, got {len(sample_tuple)}-dimensional for {sample_tuple} but expected {dimension}-dimensional")

        # validation, sample name at each index must coincide
        stacked = []
        for sample_tuple in pspace.keys():
            try:
                stacked = np.vstack([stacked, np.array([sample.name for sample in sample_tuple])])
            except ValueError:
                stacked = np.array([sample.name for sample in sample_tuple])

        if not all(len(set(stacked[:,i])) == 1 for i in range(dimension)):
            raise IndexError("sample index mismatch, all sample names at a given index must coincide")
        
        # validation, total law of probability
        all_probabilities: float = sum(pspace.values())
        try:
            sf: int = kwargs['SIGFIGS']
        except KeyError:
            sf: int = JointDistribution.SIGFIGS

        all_probabilities: float = round(all_probabilities, sf)
        if not all_probabilities == 1.0:
            raise ValueError(f"total law of probability violated, all probabilities must sum to {1.0} but got {round(all_probabilities, sf)}")

        return super(JointDistribution, cls).__new__(cls)

    def __init__(self, **kwargs) -> None:
        
        self.pspace: dict = kwargs['pspace']
        self.name: list = [sample.name for sample in next(s for s in self.pspace.keys())]
        try:
            self.SIGFIGS: int = kwargs['SIGFIGS']
        except KeyError:
            pass 

        self.dimension: int = next(len(sample_tuple) for sample_tuple in self.pspace.keys())

    def derive_marginals(self, inplace=False) -> None:
        """
        generate marginal distributions from joint distributions as RandVar objects, store marginals as list[RandVar]
            - i.e., jd(X, Y, ...) -> [mX, mY, ...]
        Note. (X, Y, ...) args in jd are not RandVar objects; the marginals [mX, mY, ...] define dependent random variables
            - marginals mX, mY, ... are RandVarBase objects
        """
        sf: int = self.SIGFIGS
        jdist_pspace: dict = self.pspace
        marginals: list = []
        for i in range(self.dimension):
            rv_name = next(sample for sample in jdist_pspace.keys())[i].name
            rv_pspace: dict = {}
            for sample_tuple, prob in jdist_pspace.items():
                sample: SampleBase = sample_tuple[i]
                try:
                    rv_pspace[sample] += prob
                except KeyError:
                    rv_pspace[sample] = prob

            marginals += [RandVarBase(**{'name': rv_name, 'pspace': rv_pspace, 'SIGFIGS': sf})]

        if inplace == True:
            return marginals
        else:
            self.marginals: list[RandVarBase] = marginals

    @property
    def margs(self):
        return self.derive_marginals(inplace=True)

    def derive_secondaries(self, inplace=False) -> None:
        """
        generate secondaries from joint distribution
            - analogue of product XY for independent random variables X, Y
            - store or return list[RandVarBase] objects
        Note. Cannot simply take product mXmY for marginals mX, mY 
            - mX, mY are assumed to be independent if extracted individually
        """
        if self.dimension == 1:
            """return RandVarBase initialised for RandVar object"""
            secondary = RandVarBase(name=(next(sample.name for sample in self.pspace.keys())[0]), pspace=self.pspace)
            secondaries = [secondary]
            if inplace == True:
                return secondaries 
            else:
                self.secondaries = secondaries
                return
        
        sf: int = self.SIGFIGS
        jdist_pspace: dict = self.pspace
        secondaries: list = []
        for i in range(self.dimension-1):
            rv_i_name = next(sample for sample in jdist_pspace.keys())[i]
            for j in range(i+1, self.dimension):
                rv_j_name = next(sample for sample in jdist_pspace.keys())[j]

                rvrv_pspace: dict = {}
                name = rv_i_name.name*rv_j_name.name
                for sample_tuple, prob in jdist_pspace.items():
                    sample_name = name
                    sample_value = sample_tuple[i].value * sample_tuple[j].value
                    sample = SampleBase(name=sample_name, value=sample_value)
                    try:
                        rvrv_pspace[sample] += prob 
                    except KeyError:
                        rvrv_pspace[sample] = prob        

                secondaries += [RandVarBase(name=name, pspace=rvrv_pspace, SIGFIGS=sf)]

        if inplace == True:
            return secondaries
        else:
            self.secondaries: list[RandVarBase] = secondaries

    @property
    def secnds(self):
        return self.derive_secondaries(inplace=True)

    def __str__(self) -> str:
        string: str = f"Joint Probability Distribution {*self.name,}"
        for sample_tuple, probability in self.pspace.items():
            string += "\n"
            for i, sample in enumerate(sample_tuple):
                if i != len(sample_tuple)-1:
                    string += f"{sample!s} AND "
                else:
                    string += f"{sample!s}"
            string += f"\t{probability = }"

        return string
    
    def to_tuple(self) -> tuple:
        """self.pspace rendered as hashable tuple"""
        pspace: dict = self.pspace
        return tuple([(s, p) for s, p in pspace.items()])

    def __eq__(self, second_joint_dist: object) -> bool:

        sf: int = max(self.SIGFIGS, second_joint_dist.SIGFIGS)
        if not set(self.name) == set(second_joint_dist):
            return False

        if not set(self.pspace.keys()) == set(second_joint_dist.pspace.keys()):
            return False
        
        for key, prob in self.pspace.items():
            if not round(second_joint_dist[key], sf) == round(prob, sf):
                return False
            
        return True

    def __hash__(self) -> int:
        return hash(self.to_tuple())
