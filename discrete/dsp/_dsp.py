import matplotlib.pyplot as plt

class DiscreteStochasticProcess:

    def __init__(self, time_steps: list[int]) -> None:
        self.time_steps: list[int] = time_steps

    def plot(self, **kwargs):
        # all processes are of RandVar objects, so they can be plotted in 2 dimensions
        title = kwargs['title']
        plt_data = kwargs['plt_data']

        plt.title(f"{title}")
        plt.xlabel("time steps")
        plt.ylabel("outcome")

        plt.plot(plt_data)
        plt.show()
