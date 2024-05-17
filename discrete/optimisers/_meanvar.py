from ..vectors import RandVec
from scipy.optimize import minimize
import numpy as np

class MeanVariance:

    def __new__(cls, rvec: RandVec, target: float):
        
        if not isinstance(rvec, RandVec):
            raise TypeError(f"{rvec} is not of type {RandVec.__name__}")
        
        if not isinstance(target, (int, float)):
            raise TypeError(f"{target} is not of type {int.__name__} or {float.__name__}")

        return super(MeanVariance, cls).__new__(cls)

    def __init__(self, rvec: RandVec, target: float) -> None:
        
        expectation_vect: np.ndarray = rvec.E
        cov_mtrx: np.ndarray = rvec.V 

        self.objective_func: function = lambda w: w.T@cov_mtrx@w
        self.constraint_1: function = lambda w: expectation_vect@w - target
        self.constraint_2: function = lambda w: sum(w) - 1

        self.bounds: list[tuple] = [(0.0, 1.0)]*rvec.dimension
        self.start: list = np.repeat([1/rvec.dimension], rvec.dimension)

    def optimise(self, **kwargs):

        objective_func: function = self.objective_func
        constraint_1: dict = {'type': 'eq', 'fun': self.constraint_1}
        constraint_2: dict = {'type': 'eq', 'fun': self.constraint_2}
        try:
            start: list = kwargs['start']
        except KeyError:
            start: list = self.start

        bounds: list[tuple] = self.bounds
        try:
            method: str = kwargs['method']
        except KeyError:
            method: str = 'SLSQP'

        minima = minimize(
                fun=objective_func,
                x0=start,
                bounds=bounds,
                method=method,
                constraints=[constraint_1, constraint_2]
            )
        
        self.success: bool = minima.success
        self.message: str = minima.message
        self.solution: list[float] = minima.x

