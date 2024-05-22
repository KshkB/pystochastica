import matplotlib.pyplot as plt
import numpy as np

class DiscreteStochasticProcess:

    def __init__(self, time_steps: list[int]) -> None:
        self.time_steps: list[int] = time_steps

    def plot_process(self, **kwargs):
        # all processes are of RandVar objects, so they can be plotted in 2 dimensions
        process: list = self.process
        x = [i for i in range(self.time_steps)]
        y = [process[i].generate(1)[0] for i in range(self.time_steps)]
        try:
            stop: int = kwargs['stop']
        except KeyError:
            stop = self.time_steps
        x = x[:stop]
        y = y[:stop]

        plt.title(f"{self.title}")
        plt.xlabel("time steps")
        plt.ylabel("outcome")

        plt.plot(x, y, **kwargs)
        plt.show()
