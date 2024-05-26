"""
implementation of calculi for Sample objects as derived from SampleBase 
calculi includes:
	- addition, subtraction, multiplication, exponentiation
	- ints or floats are converted to Decimal in order to ensure arithmetical accuracy
	- Fraction objects are kept as raw
Note:
	- Decimal + Fraction results in TypeError, this will NOT be rectified in backend 
	- user will need to manage these issues directly in scripting
"""
from ..core import SampleBase
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import sympy as sp

class Sample(SampleBase):

	def __init__(self, **kwargs) -> None:
		super().__init__(**kwargs)

	def __add__(self, second_sample):
		
		if isinstance(second_sample, (int, float, Decimal, Fraction)):
			try:
				second_sample = Decimal(str(second_sample))
			except InvalidOperation:
				"""second_sample is a Fraction object"""
				pass
			new_name = self.name + second_sample
			new_value = self.value + second_sample
		else:
			new_name = self.name + second_sample.name 
			new_value = self.value + second_sample.value

		new_name = sp.nsimplify(new_name)
		return Sample(**{'name': new_name, 'value': new_value})

	def __radd__(self, second_sample):
		return self.__add__(second_sample)
	
	def __mul__(self, second_sample):

		if isinstance(second_sample, (int, float, Decimal, Fraction)):
			try:
				second_sample = Decimal(str(second_sample))
			except InvalidOperation:
				"""second_sample is a Fractio object"""
				pass
			new_name = self.name * second_sample
			new_value = self.value * second_sample
		else:
			new_name = self.name * second_sample.name
			new_value = self.value * second_sample.value
			
		new_name = sp.nsimplify(new_name)
		return Sample(**{'name': new_name, 'value': new_value})

	def __rmul__(self, second_sample):
		return self.__mul__(second_sample)
	
	def __sub__(self, second_sample):
		second_sample = (-1)*second_sample
		return self.__add__(second_sample)
	
	def __rsub__(self, second_sample):
		neg_self = (-1)*self 
		return neg_self.__add__(second_sample)
	
	def __neg__(self):
		return (-1)*self
	
	def __pow__(self, power: int):

		new_name = self.name**power 
		new_value = self.value**power
		return Sample(**{'name': new_name, 'value': new_value})

