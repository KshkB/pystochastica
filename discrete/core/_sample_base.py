import sympy as sp
from decimal import Decimal, InvalidOperation
from fractions import Fraction

class SampleBase:

	def __new__(cls, **kwargs):
		"""
		pass dict with keys:
			- name, type sp.Expr (e.g., name = sp.Symbol('X')), representing the random variable to which this sample will be assigned
			- value, type (int, float), representing the numerical value of this sample. Note, it will be converted to float type
		"""
		name = kwargs['name']
		value = kwargs['value']

		# type validations
		if not isinstance(name, sp.Expr):
			raise TypeError(f"{name} is not of type {sp.Expr.__name__}")
		
		if not isinstance(value, (int, float, Decimal, Fraction)):
			raise TypeError(f"{value} is not of type {int.__name__}, {float.__name__}, {Decimal.__name__} or {Fraction.__name__}")

		return super(SampleBase, cls).__new__(cls)

	def __init__(self, **kwargs) -> None:
		
		self.name: sp.Expr = kwargs['name']
		try:
			self.value: Decimal = Decimal(str(kwargs['value'])) # convert int or float type to Decimal
		except InvalidOperation:
			"value passed is a Fraction object, keep as raw"
			self.value: Fraction = kwargs['value']

	# __eq__ and __hash__ ensures hashability of Sample objects
	def __eq__(self, second: object) -> bool:
		
		if not self.name == second.name:
			return False

		if not self.value == second.value:
			return False
		
		return True
	
	def __hash__(self) -> int:
		return hash(self.name) + hash(self.value)
	
	def __str__(self) -> str:
		return f"{*(self.name, self.value),}"
