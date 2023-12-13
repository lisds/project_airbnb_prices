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



def plot_with_describe(data, plot_type='hist', plot_params=None, describe_params=None, figsize=(15, 6)):
    """
    Plot a specified type of plot and display the describe() information side by side.

    Parameters:
    -----------
    data : pd.Series
        The data to be plotted and described.
    plot_type : str, optional
        The type of plot to create ('hist' for histogram, 'box' for box plot). Default is 'hist'.
    plot_params : dict, optional
        Additional parameters for the plot (e.g., bins, color, width).
    describe_params : dict, optional
        Additional parameters for the describe() table (e.g., font size).
    figsize : tuple, optional
        The size of the figure. Default is (15, 6).
    """

    # Create a subplot with 1 row and 2 columns
    fig, ax = plt.subplots(1, 2, figsize=figsize)

    if plot_type == 'hist':
        # Plot the histogram on the first subplot
        default_plot_params = {'bins': 30, 'kde': True, 'color': 'skyblue', 'element': 'step', 'stat': 'density'}
        if plot_params is not None:
            default_plot_params.update(plot_params)
        sns.histplot(data, ax=ax[0], **default_plot_params)
        ax[0].set_title('Property Distribution')
        ax[0].set_xlabel(data.name)
        ax[0].set_ylabel('Density')
        ax[0].set_xlim((min(data), max(data)))
    elif plot_type == 'box':
        # Plot the box plot on the first subplot
        default_plot_params = {'color': 'skyblue', 'width': 0.8}
        if plot_params is not None:
            default_plot_params.update(plot_params)
        sns.boxplot(data, ax=ax[0], **default_plot_params)
        ax[0].set_title('Box Plot')
        ax[0].set_ylabel(data.name)

    # Display the describe() information on the second subplot
    ax[1].axis('off')  # Turn off the axis for the describe() table
    default_describe_params = {'fontsize': 12}
    if describe_params is not None:
        default_describe_params.update(describe_params)
    ax[1].text(0, 0.5, str(data.describe()), **default_describe_params, verticalalignment='center')

    plt.show()
