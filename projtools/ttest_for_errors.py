


import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sps 
from projtools import data_tools
from scipy.spatial import distance
from projtools import k_best_neighbours_prediction



#var1 = 'accommodates'
#var2 = 'number_of_reviews'
#var3 = 'host_listings_count'
#varZ = 'price_per_night_£'
#ID_Z = 17402
data = data_tools.data_setup()

def overprice_function(var1, var2, var3, ID_Z, num_rows, significance):
    numerical_data = data_tools.group_data(data,'numerical')
    relevant = numerical_data[[var1, var2, var3, 'price_per_night_£']].dropna()
    for index, row in relevant.head(num_rows).iterrows():
        error = k_best_neighbours_prediction.prediction_func_location(var1, var2, var3, 'price_per_night_£', ID_Z)
        relevant.at[index, 'errors'] = error
    ID_Z_error = relevant.at[ID_Z, 'errors']
    likelihood = np.count_nonzero(relevant['errors'] < ID_Z_error) / num_rows
    if likelihood > 1 - significance:
        print('This listing is overpriced for its characteristics and location based on you significance level according to the deviation values of x rows')
    else:
        print('This listing is not overpriced for its characteristics and location based on you significance level according to the deviation values of x rows')
    print(likelihood)
    return error






def ttest_function(var1, var2, var3, ID_Z, rows):
    numerical_data = data_tools.group_data(data,'numerical')
    relevant = numerical_data[[var1, var2, var3, 'price_per_night_£']].dropna()
    for index, row in relevant.head(rows).iterrows():
        error = k_best_neighbours_prediction.prediction_func_location('accommodates', 'number_of_reviews', 'host_listings_count', 'price_per_night_£', index)
        relevant.at[index, 'errors'] = error
    ID_Z_error = relevant.at[ID_Z, 'errors']
    likelihood = np.count_nonzero(relevant['errors'] > ID_Z_error) / rows
    if likelihood < 0.10:
        print('This listing is overpriced for its characteristics and location')
    else:
        print('This listing is not overpriced for its characteristics and location')
    



# higher prices seem to occur at 1 year and 3 years 

# look at the spread of the other days and the quantitity - see if this is the same as the spread for the quantity at 1 year and 3 years 

# def ttest_func(error_value, var1, var2, var3, varZ, ID_Z):

# need to provide the error takes the error and then performs a simple ttest that runs a prediction for every value and thn