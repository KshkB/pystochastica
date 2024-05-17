from ..core import JointDistribution
from ..variables import RandVar
from ..utils import generate_jdist
import numpy as np

def randvar_base_descent(*randvarbases) -> list[RandVar]:
    return [RandVar(name=rv.name, pspace=rv.pspace) for rv in randvarbases]
class RandVec(JointDistribution):

    def __init__(self, **joint_pspace: dict) -> None:
        super().__init__(**joint_pspace)

        # generate random vector components
        self.derive_marginals()
        self.derive_secondaries()

        # Descent, RandvarBase --> RandVar, to fill random vector components
        self.components: np.ndarray = np.array(randvar_base_descent(*self.marginals))
        self.secondaries: np.ndarray = np.array(randvar_base_descent(*self.secondaries))

    def __add__(self, second_randvec):
        """
        WARNING: RandVec1 + RandVec2 assumes RandVec1 and RandVec2 are independent random vectors (c.f., RandVar.__add__)
            - independence means, for all i, component RandVec1_i is independent of RandVec2_i
            - if RandVec1 and RandVec2 are dependent, initialise a new random vector with desired dependency among components
        """
        if isinstance(second_randvec, (list, np.ndarray)): # pass list[float] or np.ndarray with np.array.shape = (self.dimension,)
            new_pspace: dict = {}
            for sample_tuple, prob in self.pspace.items():
                new_tuple = tuple([sample_tuple[i] + second_randvec[i] for i in range(self.dimension)])
                try:
                    new_pspace[new_tuple] += prob
                except KeyError:
                    new_pspace[new_tuple] = prob 
        else:
            new_marginals = [self.components[i] + second_randvec.components[i] for i in range(self.dimension)]
            new_pspace = generate_jdist(*new_marginals)
        
        return RandVec(pspace=new_pspace)

    def __radd__(self, second_randvec):
        return self.__add__(second_randvec)

    def __mul__(self, randvar):
        """
        multiply by (int, float) or RandVar object
            - random vectors form a module over the algebra of random variables (c.f., functions on vector spaces)
            - randvar is assumed to be independent of components in self.components
        """
        if isinstance(randvar, (int, float)):
            sf = self.SIGFIGS
            randvar = round(randvar, sf)
            new_pspace: dict = {
                (randvar*s for s in sample): prob for sample, prob in self.pspace.items()
                }
        else:
            sf: int = max(self.SIGFIGS, randvar.SIGFIGS)
            new_pspace: dict = {}
            for rv_sample, rv_prob in randvar.pspace.items():
                for sample, prob in self.pspace.items():
                    new_tup = tuple([rv_sample] + list(sample))
                    new_prob = rv_prob*prob 
                    new_pspace[new_tup] = new_prob

        return RandVec(pspace=new_pspace)

    def __sub__(self, second_rvec):
        second_rvec = (-1)*second_rvec
        return self.__add__(second_rvec)
    
    def __rsub__(self, second_rvec):
        neg_self = (-1)*self 
        return neg_self.__add__(second_rvec)
    
    def __neg__(self):
        return (-1)*self

    def dot(self, second_rvec):
        """
        returns RandVar object
            - this is the component sum of dependent random variables (marginals)
        """
        new_pspace: dict = {}
        if isinstance(second_rvec, (list, np.ndarray)):
            new_name = np.array([sample.name for sample in next(sample_tup for sample_tup in self.pspace.keys())])@second_rvec
            for sample_tup, prob in self.pspace.items():
                new_sample = np.array(sample_tup)@second_rvec
                try:
                    new_pspace[new_sample] += prob
                except KeyError:
                    new_pspace[new_sample] = prob

            return RandVar(**{'name': new_name, 'pspace': new_pspace, 'SIGFIGS': self.SIGFIGS})

        new_name = np.array([sample.name for sample in next(sample_tup for sample_tup in self.pspace.keys())])\
                    @ np.array([sample.name for sample in next(sample_tup for sample_tup in second_rvec.pspace.keys())])
        for sample_tup, prob in self.pspace.items():
            for second_sample_tup, second_prob in second_rvec.pspace.items():
                new_sample = np.array(sample_tup) @ np.array(second_sample_tup)
                new_prob = prob*second_prob
                try:
                    new_pspace[new_sample] += new_prob
                except KeyError:
                    new_pspace[new_sample] = new_prob

        return RandVar(**{'name': new_name, 'pspace': new_pspace, 'SIGFIGS': self.SIGFIGS})
    
    def sum(self):
        return self.dot(np.ones(self.dimension))

    def __matmul__(self, second_rvec):
        return self.dot(second_rvec)

    def calculate_expectation(self, inplace=False) -> None:
        expectation_vector = []
        for rv in self.components:
            if inplace == False:
                rv.calculate_expectation()
            else:
                expectation_vector += [rv.calculate_expectation(inplace=inplace)]
        
        if inplace == False:
            self.expectation: list[float] = [rv.expectation for rv in self.components]
        else:
            return expectation_vector
    
    @property
    def E(self):
        return np.array(self.calculate_expectation(inplace=True))

    def calculate_variance(self, inplace=False) -> None:
        components: np.ndarray = self.components
        secondaries: np.ndarray = self.secondaries

        cov_mtrx = np.full((self.dimension, self.dimension), np.nan)
        for i, component in enumerate(components):
            for j, second_component in enumerate(components[i:]): # components[i:] includes components[i]
                if j == 0:
                    cov_mtrx[i, i] = component.V
                else:
                    it = iter(secondaries)
                    secondary = next(s for s in it if s.name == component.name*second_component.name)
                    cov_mtrx[i, i+j] = secondary.E - component.E*second_component.E
                    cov_mtrx[i+j, i] = cov_mtrx[i, i+j]

        cov_mtrx = np.around(cov_mtrx, self.SIGFIGS)
        if inplace == False:
            self.cov_mtrx = cov_mtrx
        else:
            return cov_mtrx

    @property
    def V(self):
        return self.calculate_variance(inplace=True)

    def Prob(self, predicate: list[str]) -> float:
        """
        predicate ['<= x', '>= y', '== z', ...], calculates joint probability Pr(X <= x, Y => y, Z == z, ...)
            - ensure len(predicate) == self.dimension or predicate is str
            - if e.g., predicate = '<= 1.0', calculates joint probability Pr(X <= 1.0, Y => 1.0, Z == 1.0, ...)
            - arg predicate = ['== True']*self.dimension returns 1.0
        """
        if isinstance(predicate, str):
            return self.Prob([predicate]*self.dimension)

        rsult: float = 0.0
        for sample_tuple, prob in self.pspace.items():
            if all(eval(f"{sample_tuple[i].value}" + predicate[i]) for i in range(self.dimension)):
                rsult += prob

        return round(rsult, self.SIGFIGS)