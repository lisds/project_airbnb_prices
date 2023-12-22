import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_scatter_quartiles_multiple_dfs(dataframes, column_name, df_names):
    plt.figure(figsize=(10, 6))

    # different colours for each dataframe scatter 
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown']

    # sperate points fro the scatter 
    offset = 0.1
    x_positions = np.array([1, 2, 3, 4])

    for idx, df in enumerate(dataframes):
        # workout the quartiles 
        Q1 = df[column_name].quantile(0.25)
        Q2 = df[column_name].quantile(0.5) 
        Q3 = df[column_name].quantile(0.75)

      # sperate into quartiles
        def determine_quartile(value):
            if value <= Q1:
                return 1  
            elif value <= Q2:
                return 2  
            elif value <= Q3:
                return 3  
            else:
                return 4  

        # create the quartile column to use
        df['Quartile'] = df[column_name].apply(determine_quartile)

        # do sccatter
        plt.scatter(df['Quartile'] + (idx - len(dataframes)/2) * offset, df[column_name], alpha=0.5, color=colors[idx], label=df_names[idx])

    plt.xlabel('Quartiles')
    plt.ylabel(column_name)
    plt.title(f'Scatter Plot of {column_name} Values in Each Quartile Across Multiple DataFrames')
    
    plt.ylim(0,1700)
    plt.legend()
    plt.show()


def plot_scatter_quartiles_multiple_dfs(dataframes, column_name, df_names):
    plt.figure(figsize=(10, 6))

    # different colours for each dataframe scatter 
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown']

    # sperate points fro the scatter 
    offset = 0.1
    x_positions = np.array([1, 2, 3, 4])

    for idx, df in enumerate(dataframes):
        # workout the quartiles 
        Q1 = df[column_name].quantile(0.25)
        Q2 = df[column_name].quantile(0.5) 
        Q3 = df[column_name].quantile(0.75)

      # sperate into quartiles
        def determine_quartile(value):
            if value <= Q1:
                return 1  
            elif value <= Q2:
                return 2  
            elif value <= Q3:
                return 3  
            else:
                return 4  

        # create the quartile column to use
        df['Quartile'] = df[column_name].apply(determine_quartile)

        # do sccatter
        plt.scatter(df['Quartile'] + (idx - len(dataframes)/2) * offset, df[column_name], alpha=0.5, color=colors[idx], label=df_names[idx])

    plt.xlabel('Quartiles')
    plt.ylabel(column_name)
    plt.title(f'Scatter Plot of {column_name} Values in Each Quartile Across Multiple DataFrames')
    plt.legend()
    plt.show()