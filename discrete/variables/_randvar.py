"""
implementation of calculi for discrete RandVar objects (= discrete random variables)
calculi implemented:
	- addition, subtraction, multiplication, exponentiation
	- moments (expectation, variance, higher moments, higher shifted moments)
functionality:
	- storage for joint distributions with other RandVar objects as set
	- joint_distributions facilitate lookups to implement calculi for dependent random variables
	- warning: for more than two dependent random variables, use RandVec objects
"""
from ..core import RandVarBase
from ..samples import Sample
from ..simulations import RandVarSimulator
from ..utils import convolve_dicts, dict_mul
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import numpy as np
import sympy as sp

class RandVar(RandVarBase):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def __add__(self, second_rv):
		"""assumes self and second_rv are independent, use RandVec for dependent variables"""
		if isinstance(second_rv, (int, float, Decimal, Fraction)):
			try:
				second_rv = Decimal(str(second_rv))
			except InvalidOperation:
				"""second_rv is a Fraction object"""
				pass
			new_name = self.name + second_rv
			new_pspace: dict = {sample + second_rv: prob for sample, prob in self.pspace.items()}
		else:
			new_name = self.name + second_rv.name 
			if new_name == 0:
				raise ValueError("use the RandVec data type to subract self from self")
			
			new_pspace_dict: dict = convolve_dicts(
					{sample.value: prob for sample, prob in self.pspace.items()}, 
					{sample.value: prob for sample, prob in second_rv.pspace.items()}
				)
			new_pspace: dict = {
					Sample(**{'name': new_name, 'value': value}): prob for value, prob in new_pspace_dict.items()
				}
		new_name = sp.nsimplify(new_name)
		return RandVar(**{'name': new_name, 'pspace': new_pspace})
	
	def __radd__(self, second_rv):
		return self.__add__(second_rv)
	
	def __mul__(self, second_rv):
		"""assumes self and second_rv are independent, use RandVec for dependent variables"""
		if isinstance(second_rv, (int, float, Decimal, Fraction)):
			try:
				second_rv = Decimal(str(second_rv))
			except InvalidOperation:
				"""second_rv is a Fraction object"""
				pass
			new_name = second_rv * self.name
			new_pspace = {second_rv * sample: prob for sample, prob in self.pspace.items()}
		else:
			new_name = self.name*second_rv.name
			new_pspace_dict: dict = dict_mul(
					{sample.value: prob for sample, prob in self.pspace.items()},
					{sample.value: prob for sample, prob in second_rv.pspace.items()}
				)
			new_pspace: dict = {
					Sample(**{'name': new_name, 'value': value}): prob for value, prob in new_pspace_dict.items()
				}
		new_name = sp.nsimplify(new_name)
		return RandVar(**{'name': new_name, 'pspace': new_pspace})
	
	def __rmul__(self, second_rv):
		return self.__mul__(second_rv)

	def __sub__(self, second_rv):
		second_rv = (-1)*second_rv
		return self.__add__(second_rv)
	
	def __rsub__(self, second_rv):
		neg_self = (-1)*self 
		return neg_self.__add__(second_rv)
	
	def __neg__(self):
		return (-1)*self

	def __pow__(self, power):

		if power == 1:
			return self 
		
		new_name = self.name**power
		new_pspace: dict = {}
		for sample, prob in self.pspace.items():
			try:
				new_pspace[sample**power] += prob
			except KeyError:
				new_pspace[sample**power] = prob
		return RandVar(**{'name': new_name, 'pspace': new_pspace})

	def calculate_expectation(self, inplace=False) -> None:
		
		expectation: Decimal = Decimal('0.0')
		for sample, prob in self.pspace.items():
			try:
				expectation += sample.value * prob
			except TypeError:
				expectation: float = float(expectation)
				expectation += float(sample.value) * prob

		expectation: float = float(expectation) # store as float object, not Decimal
		if inplace == True:
			return expectation
		else:
			self.expectation: float = expectation

	@property
	def E(self):
		return self.calculate_expectation(inplace=True)

	def calculate_variance(self, inplace=False) -> None:

		square_expectation: Decimal = Decimal('0.0')
		for sample, prob in self.pspace.items():
			try:
				square_expectation += (sample.value**2) * prob
			except TypeError:
				square_expectation: float = float(square_expectation)
				square_expectation += (float(sample.value)**2) * prob

		square_expectation: float = float(square_expectation)
		expectation: float = self.E
		if inplace==True: 
			# inplace is True, do not store output
			return square_expectation - expectation**2
		else:
			# inplace is False, store output as class attr
			self.variance: float = square_expectation - expectation**2
		
	@property 
	def V(self):
		return self.calculate_variance(inplace=True)
	
	def Prob(self, predicate: str) -> float:
		rsult: Decimal = Decimal('0.0')
		for sample, prob in self.pspace.items():
			stmnt = f"{sample.value}" + predicate
			if eval(stmnt):
				try:
					rsult += prob
				except TypeError:
					rsult: float = float(rsult)
					rsult += prob
			else:
				pass 

		return rsult

	def generate(self, iterations: int) -> np.ndarray:
		sample_values = [sample.value for sample in self.pspace.keys()]
		probabilities = list(self.pspace.values())
		out = np.random.choice(sample_values, iterations, probabilities)

		return out

	def pdf(self, **kwargs):
		rv_sim = RandVarSimulator(**kwargs)
		rv_sim.pdfs(self)

	def cdf(self, **kwargs):
		rv_sim = RandVarSimulator(**kwargs)
		rv_sim.cdfs(self)
