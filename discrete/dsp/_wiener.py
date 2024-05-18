from ._dsp import DiscreteStochasticProcess as DSP
from ..variables import RandVar

class Wiener(DSP):

    def __init__(self, times: list[int], acc: int) -> None:
        super().__init__(times)
        rv = 0
        for _ in range(int()):
            ...
        self.process = ...