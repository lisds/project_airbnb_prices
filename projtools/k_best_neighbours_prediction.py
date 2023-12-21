import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sps 
from projtools import data_tools
from scipy.spatial import distance

# the aim of the following is to create a suggestion of what a value should be based on the results of its nearest neighbours and then to run 
#   a ttest that will suggest whether the difference between the predicted and the actual is significant enough to suggest that something is going wrong

# example input 

# var1 = 'accommodates'
# var2 = 'number_of_reviews'
# var3 = 'host_listings_count'
# varZ = 'price_per_night_£'
# ID_Z = 106332


data = data_tools.data_setup()

def prediction_func(var1, var2, var3, varZ, ID_Z):
    def un_standardise(standardised_value, original_mean, original_std):
        return (standardised_value * original_std) + original_mean
    numerical_data = data_tools.group_data(data,'numerical')
    relevant = numerical_data[[var1, var2, var3, varZ]].dropna()
    standardised_relevant_data = (relevant - relevant.mean()) / relevant.std()
    variable_df = standardised_relevant_data
    row_Z = variable_df.loc[ID_Z, [var1, var2, var3]]
    variable_df.drop(ID_Z)
    def calculate_similarity(row):
        return distance.euclidean(row[[var1, var2, var3]], row_Z)
    distances = variable_df.head(1000).apply(calculate_similarity, axis=1)
    closest = list(distances.sort_values(ascending=True).head().index)
    standard_prediction = variable_df.loc[closest, varZ].mean()
    standard_actual = variable_df.loc[ID_Z, varZ]
    prediction = un_standardise(standard_prediction, relevant[varZ].mean(), relevant[varZ].std())
    actual = un_standardise(standard_actual, relevant[varZ].mean(), relevant[varZ].std())
    #prediction_text = "Prediction for {} {}".format(ID_Z, varZ)
    #actual_text = "Actual {} for {}".format(varZ, ID_Z)
    #print(prediction_text, round(prediction,2))
    #print(actual_text, round(actual,2))
    standardised_Z_difference = standard_actual - standard_prediction   
    Z_difference = actual - prediction
    #print("Error", round(Z_difference,2))
    return Z_difference

    # var 1, 2 and 3 are the predictor variables 
    # var Z is the variable of interest - the one you want to predict 
    # ID_Z is the property number that you want to get a prediction on
    
    
    
    # return()