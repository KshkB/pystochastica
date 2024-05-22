from ._sample_base import SampleBase
import sympy as sp
from decimal import Decimal

class RandVarBase:

	SIGFIGS: int = 5 # default numerical accuracy for probabilities

	def __new__(cls, **kwargs):
		
		# necessary keys to pass
		name = kwargs['name']
		pspace: dict = kwargs['pspace']

		# type validation for name
		if not isinstance(name, sp.Expr):
			raise TypeError(f"{name} is not a {sp.Expr.__name__} type object")

		# set validation, keys must be unique
		pspace_keys = pspace.keys()
		if not len(set(pspace_keys)) == len(pspace_keys):
			raise ValueError("not all samples are unique")

		# pspace validation, keys are Sample objects, values are probabilities
		sf: int = RandVarBase.SIGFIGS
		for sample, probability in pspace.items():

			if not isinstance(sample, SampleBase):
				raise TypeError(f"{sample} is not a {SampleBase.__name__} type object")
			if not sample.name == name:
				raise NameError(f"{sample} erroneously assigned to {name}")
			
			probability_rounded = round(probability, sf)
			if not (0 <= probability_rounded and probability_rounded <= 1):
				raise ValueError(f"{probability} is not a valid probability")

		# validation, total law of probability
		all_probabilities: list[float] = pspace.values()
		total: float = round(sum(all_probabilities), sf)
		if not total == 1.0:
			raise ValueError(f"total law of probability violated, got {total} but expected {1.0}")

		return super(RandVarBase, cls).__new__(cls)

	def __init__(self, **kwargs):
		
		try:
			self.SIGFIGS: int = kwargs['SIGFIGS']
		except KeyError:
			pass 

		self.name: sp.Expr = kwargs['name']
		self.pspace: dict = {k: v for k, v in kwargs['pspace'].items() if round(v, self.SIGFIGS) != 0}

	def to_tuple(self) -> tuple:
		"""cast pspace to a tuple object"""
		pspace = self.pspace
		return tuple([(k, round(v, self.SIGFIGS)) for k, v in pspace.items()])

	def __eq__(self, second_rv: object) -> bool:

		if not self.name == second_rv.name:
			return False

		if not self.to_tuple() == second_rv.to_tuple():
			return False
		
		return True

	def __hash__(self) -> int:
		name = self.name 
		pspace_tuple: tuple = self.to_tuple()
		return hash(name) + hash(pspace_tuple)
	
	def __str__(self) -> str:
		string: str = f"Random variable {self.name}"
		for sample, probability in self.pspace.items():
			probability = round(probability, self.SIGFIGS)
			string += f"\n{sample}\t{probability = }"

		return string