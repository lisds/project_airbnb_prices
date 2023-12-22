# projtools/plotting_tools.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def Distribution_of_Listings_Among_Hosts(host_listing_counts):
    """
    Plot the distribution of listings per host.

    Parameters:
    - host_listing_counts

    """
    # Binning data
    bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 50, 100, float('inf')]
    bin_labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10-20', '21-50', '51-100', '101+']
    binned_counts = pd.cut(host_listing_counts, bins, labels=bin_labels, right=False)
    binned_counts_value = binned_counts.value_counts().sort_index()

    # Plot the binned data
    plt.figure(figsize=(12, 6))
    plt.bar(binned_counts_value.index, binned_counts_value.values, width=0.5, edgecolor="black")
    plt.xlabel('Number of Listings')
    plt.ylabel('Number of Hosts')
    plt.title('Distribution of Listings Among Hosts')
    plt.yscale('log')
    plt.show()

def Market_Share_by_Host_Groups(host_listing_counts, top_1_percent_threshold, total_listings):
    """
    Plot the market share by host groups (top 1% vs. remaining 99%).

    Parameters:
    - host_listing_counts
    - top_1_percent_threshold
    - total_listings

    """
    # The first bin will be for hosts not in the top 1%, and the second for those in the top 1%
    bins = [0, top_1_percent_threshold, host_listing_counts.max()]
    bin_labels = ['99% of Hosts', '1% of Hosts']

    # Bin the data
    binned_counts = pd.cut(host_listing_counts, bins, labels=bin_labels)
    binned_counts_value = binned_counts.value_counts().sort_index()

    # Calculate market share
    market_share = host_listing_counts.groupby(binned_counts, observed=True).sum() / total_listings * 100

    # Plot market share
    plt.figure(figsize=(10, 6))
    market_share.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.xlabel('Host Groups')
    plt.ylabel('Percentage of Total Listings')
    plt.title('Market Share by Host Groups')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def Plot_Average_Max_Nights_Booked_Distribution(data):
    """
    Create and display a histogram plot for the distribution of average maximum nights booked.

    Parameters: 
    max_night_avg_bookings

    """
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.histplot(data['maximum_nights_avg_bookings'], kde=True, bins=50)
    plt.title('Distribution of Average Maximum Nights Booked')
    plt.xlabel('Average Maximum Nights')
    plt.ylabel('Frequency')

    # Show the plot
    plt.show()

def Price_Per_Night_Distribution(data):
    """
    Create a scatter plot to visualize the relationship between
    price per night and average maximum nights for bookings over 90 days.

    Parameters:
    long_term_listings

    Returns:
    - None (displays the scatter plot).
    """
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x=data['maximum_nights_avg_bookings'], y=data['price_per_night_£'])
    plt.title('Price per Night vs. Average Maximum Nights for Bookings Over 90 Days')
    plt.xlabel('Average Maximum Nights Booked (Over 90 Days)')
    plt.ylabel('Price per Night (£)')
    plt.show()

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
