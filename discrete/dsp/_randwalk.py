from ._dsp import DiscreteStochasticProcess as DSP
from ..variables import RandVar
from ..samples import Sample
import sympy as sp

class RandWalk(DSP):

    # custom probabilities
    p: float = 0.5
    q: float = 0.5

    def __init__(self, time_steps: list[int], **kwargs) -> None:
        super().__init__(time_steps)

        # pass custom probabilities p, q if desired; ensure p + q = 1
        try:
            self.p = kwargs['p']
            self.q = kwargs['q']
        except KeyError:
            pass 

    def run(self) -> list:
        """
        once initialised, run process for time_steps-many steps
            - at each step, create RandVar object and generate a sample
            - return output as list[float]
        """
        out: list = [0] # starting output is always 0
        rv = 0
        for i in range(self.time_steps-1):
            name = sp.Symbol(f"X_{i}")
            pspace: dict = {Sample(name=name, value=-1): self.p, Sample(name=name, value=1): self.q}
            rv += RandVar(**{'name': name, 'pspace': pspace})
            out += [rv.generate(1)[0]]

        self.out: list = out

    def plt(self):
        self.run()
        self.plot(
            title=f'Random walk after {self.time_steps} steps',
            plt_data=self.out)
