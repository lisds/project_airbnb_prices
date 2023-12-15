# projtools/plotting_tools.py

import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib.pyplot as plt
import seaborn as sns

def plot(series, plot_name, plot_type='hist', bins=30, kde=True, color='skyblue', figsize=(10, 6)):
    """
    Plot the distribution of a Series.

    Parameters:
    -----------
    series : pd.Series
        The Series to be plotted.
    plot_name : str
        The title of the plot.
    plot_type : str, optional
        The type of plot to create ('hist' for histogram, 'kde' for kernel density estimate, 'box' for box plot). Default is 'hist'.
    bins : int, optional
        The number of bins in the histogram. Default is 30.
    kde : bool, optional
        Whether to add a kernel density estimate. Default is True.
    color : str, optional
        The color of the plot. Default is 'skyblue'.
    figsize : tuple, optional
        The size of the figure. Default is (10, 6).
    """

    plt.figure(figsize=figsize)

    if plot_type == 'hist':
        sns.histplot(series, bins=bins, kde=kde, color=color)
        plt.ylabel('Frequency')
    elif plot_type == 'kde':
        sns.kdeplot(series, color=color)
        plt.ylabel('Density')
    elif plot_type == 'box':
        sns.boxplot(series, color=color)
        plt.ylabel(series.name)  # Use the column name as the y-axis label
    else:
        raise ValueError("Invalid plot_type. Choose from 'hist', 'kde', or 'box'.")

    plt.title(plot_name)
    plt.xlabel(series.name)  # Use the column name as the x-axis label
    plt.show()

