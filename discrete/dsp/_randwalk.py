from ._dsp import DiscreteStochasticProcess as DSP
from ..variables import RandVar
from ..samples import Sample
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

class RandWalk(DSP):

    # custom probabilities
    p: float = 0.5
    q: float = 0.5

    def __init__(self, time_steps: list[int], **kwargs) -> None:
        super().__init__(time_steps)
        self.title = f"{RandWalk.__name__}"

        # pass custom probabilities p, q if desired; ensure p + q = 1
        try:
            self.p = kwargs['p']
            self.q = kwargs['q']
        except KeyError:
            pass 

    def generate_process(self) -> list:
        """
        once initialised, run process for time_steps-many steps
            - at each step, create RandVar object and generate a sample
            - return output as list[float]
        """
        name = sp.Symbol('0')
        rv = RandVar(**{'name': name, 'pspace': {Sample(name=name, value=0): 1.0}})
        process: list = [rv]
        for i in range(self.time_steps-1):
            name = sp.Symbol(f"X_{i}")
            pspace: dict = {Sample(name=name, value=-1): self.p, Sample(name=name, value=1): self.q}
            rv += RandVar(**{'name': name, 'pspace': pspace})
            process += [rv]

        self.process: list = process

    def plt(self):
        self.generate_process()
        self.plot_process()

    def walk_data(self, steps: int) -> np.ndarray:
        name = sp.Symbol('X')
        rv = RandVar(**{'name': name, 'pspace': {Sample(name=name, value=1): self.p, Sample(name=name, value=-1): self.q}})
        out = rv.generate(iterations=steps)
        out = np.insert(out, 0, 0)
        return out.cumsum()       

    def plt_walk(self, steps: int) -> None:
        y = self.walk_data(steps)

        plt.title("Random walk")
        plt.xlabel("Steps")
        plt.ylabel("Net distance")
        plt.plot(y)        
        plt.show()
    
    def plt_walks(self, steps: int, **kwargs) -> None:
        """plot walks on self.time_steps many subplots"""
        time_steps: int = self.time_steps
        if time_steps == 1:
            return self.plt_walk()
        
        try:
            ncols: int = kwargs['ncols']
            nrows: int = kwargs['nrows']
        except KeyError:
            ncols = 2
            nrows = sum(divmod(time_steps, ncols))

        fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=(15, 8), squeeze=False)
        fig.suptitle(f"{time_steps} Random Walks")
        for i in range(nrows):
            for j in range(ncols):
                try:
                    index = ncols*i + j
                    y: np.ndarray = self.walk_data(steps)
                    axs[i, j].set_title(f"Walk no. {index+1}")
                    axs[i, j].set_xlabel("steps")
                    axs[i, j].set_ylabel("net distance")
                    axs[i, j].plot(y)

                except IndexError:
                    axs[i, j].axis("off")
        
        plt.tight_layout()
        plt.show()
