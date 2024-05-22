from ..core import RandVarBase
import matplotlib.pyplot as plt

class RandVarSimulator:

    FIGSIZE: tuple = (15, 9) # default figsize
    ITERATIONS: int = 1000 # default iterations

    def __init__(self, **kwargs) -> None:
        """initialise defaults unless config arguments otherwise passed"""

        # get kwargs for configuration if any passed
        try:
            self.ITERATIONS = kwargs['iterations']
        except KeyError:
            pass 

        try:
            self.FIGSIZE: tuple = kwargs['FIGSIZE']
        except KeyError:
            pass

    def plot(self, *randvars, **kwargs) -> None:
        if not all(isinstance(randvar, RandVarBase) for randvar in randvars):
            raise TypeError(f"not all arguments passed are {RandVarBase.__name__} objects")
        
        iterations: int = self.ITERATIONS
        ncols: int = 1 if len(randvars) == 1 else 2
        nrows: int = sum(divmod(len(randvars), 2))
        fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=self.FIGSIZE, squeeze=False)

        # get data from kwargs
        title: str = kwargs['title'] + f" after {iterations = }"
        plot_title: str = kwargs['plot_title']
        xlabel: str = kwargs['xlabel']
        ylabel: str = kwargs['ylabel']
        plt_data: dict = kwargs['plt_data']
        plt_type: str = kwargs['plt_type']
        plt_kwargs: dict = kwargs['plt_kwargs']

        # generate subplots
        fig.suptitle(f"{title}")
        for i in range(nrows):
            for j in range(ncols):
                try:
                    index: int = ncols*i + j
                    randvar = randvars[index]
                    randvar_plt_data = plt_data[randvar]

                    x = randvar_plt_data['x']
                    y = randvar_plt_data['y']
                    axs[i, j].set_title(f"{plot_title} for {randvar.name}")
                    axs[i, j].set_xlabel(f"{xlabel}")
                    axs[i, j].set_xticks(x)
                    axs[i, j].set_ylabel(f"{ylabel}")
                    getattr(axs[i, j], f'{plt_type}')(x, y, **plt_kwargs)
                except IndexError:
                    axs[i, j].axis("off")

        plt.tight_layout()
        plt.show()

    def pdfs(self, *randvars):
        # generate plot data for pdf plots
        plt_data: dict = {}
        for randvar in randvars:
            plt_data[randvar] = {}
            rv_outcomes = {sample.value: 0 for sample in randvar.pspace}
            outcomes: list = randvar.generate(self.ITERATIONS)
            for outcome in outcomes:
                rv_outcomes[outcome] += 1
            
            rv_outcomes = dict(sorted(rv_outcomes.items())) # sorted by key
            plt_data[randvar]['x'] = list(rv_outcomes.keys())
            plt_data[randvar]['y'] = list(rv_outcomes.values())
            plt_type: str = 'bar'
            plt_kwargs: dict = {'width': 0.95}

        # return self.plot()
        self.plot(*randvars, **{
            'title': f"Probability distributions for {', '.join([f'{rv.name}' for rv in randvars])}",
            'plot_title': 'Probability distribution',
            'xlabel': 'outcomes',
            'ylabel': 'frequency',
            'plt_data': plt_data,
            'plt_type': plt_type,
            'plt_kwargs': plt_kwargs
            })

    def cdfs(self, *randvars):
        # generate plot data for cdf plots
        plt_data: dict = {}
        for randvar in randvars:
            plt_data[randvar] = {}
            x = sorted([sample.value for sample in randvar.pspace])
            y = [randvar.Prob(f'<= {val}') for val in x]
            plt_data[randvar]['x'] = x
            plt_data[randvar]['y'] = y 
            plt_type: str = 'plot'
            plt_kwargs: dict = {'c': 'r'}

        self.plot(*randvars, **{
            'title': f"Cumulative distribution for {', '.join([f'{rv.name}' for rv in randvars])}",
            'plot_title': 'Cumulative distribution',
            'xlabel': 'outcomes',
            'ylabel': 'probability',
            'plt_data': plt_data,
            'plt_type': plt_type,
            'plt_kwargs': plt_kwargs
            })



