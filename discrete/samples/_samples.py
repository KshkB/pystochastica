from ..core import SampleBase
# from core import SampleBase
"""
implementation of calculi for Sample objects as derived from SampleBase 
calculi includes:
	- addition, subtraction, multiplication, exponentiation 
"""
class Sample(SampleBase):

	def __init__(self, **kwargs) -> None:
		super().__init__(**kwargs)

	def __add__(self, second_sample):
		
		if isinstance(second_sample, (int, float)):
			sf: int = self.SIGFIGS
			second_sample = round(second_sample, sf)

			new_name = self.name + second_sample
			new_value = round(self.value + second_sample, sf)
		else:
			sf: int = max(self.SIGFIGS, second_sample.SIGFIGS)

			new_name = self.name + second_sample.name 
			new_value = round(self.value + second_sample.value, sf)

		return Sample(**{'name': new_name, 'value': new_value, 'SIGFIGS': sf})

	def __radd__(self, second_sample):
		return self.__add__(second_sample)
	
	def __mul__(self, second_sample):

		if isinstance(second_sample, (int, float)):
			sf: int = self.SIGFIGS
			second_sample = round(second_sample, sf)

			new_name = self.name * second_sample
			new_value = round(self.value * second_sample, sf)
		else:
			sf: int = max(self.SIGFIGS, second_sample.SIGFIGS)
			
			new_name = self.name * second_sample.name
			new_value = round(self.value * second_sample.value, sf)

		return Sample(**{'name': new_name, 'value': new_value, 'SIGFIGS': sf})

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

