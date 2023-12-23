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

def prediction_func_diff(var1, var2, var3, varZ, ID_Z):
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

def prediction_func_prediction(var1, var2, var3, varZ, ID_Z):
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
    prediction_text = "Prediction for {} {}".format(ID_Z, varZ)
    actual_text = "Actual {} for {}".format(varZ, ID_Z)
    #print(prediction_text, round(prediction,2))
    #print(actual_text, round(actual,2))
    standardised_Z_difference = standard_actual - standard_prediction   
    Z_difference = actual - prediction
    return Z_difference

def prediction_func_location(var1, var2, var3, varZ, ID_Z):
    def un_standardise(standardised_value, original_mean, original_std):
        return (standardised_value * original_std) + original_mean
    location_specific = data[data['neighbourhood_location'] == data.loc[ID_Z, 'neighbourhood_location']]
    location_numerical = data_tools.group_data(location_specific,'numerical')
    relevant = location_numerical[[var1, var2, var3, varZ]].dropna()
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
    prediction_text = "Prediction for {} {}".format(ID_Z, varZ)
    actual_text = "Actual for {} {}".format(varZ, ID_Z)
    #print(prediction_text, round(prediction,2))
    #print(actual_text, round(actual,2))
    #standardised_Z_difference = standard_actual - standard_prediction   
    Z_difference = actual - prediction
    #print("Error", round(Z_difference,2))
    return Z_difference
    



def ninety_day_test(ID_Z):
    def un_standardise(standardised_value, original_mean, original_std):
        return (standardised_value * original_std) + original_mean
    numerical_data = data_tools.group_data(data,'numerical')
    relevant = numerical_data[['bedrooms', 'price_per_night_£', 'host_listings_count', 'maximum_nights_avg_bookings']].dropna()
    standardised_relevant_data = (relevant - relevant.mean()) / relevant.std()
    variable_df = standardised_relevant_data
    row_Z = variable_df.loc[ID_Z, ['bedrooms', 'price_per_night_£', 'host_listings_count']]
    variable_df.drop(ID_Z)
    def calculate_similarity(row):
        return distance.euclidean(row[['bedrooms', 'price_per_night_£', 'host_listings_count']], row_Z)
    distances = variable_df.sample(1000, replace=True).apply(calculate_similarity, axis=1)
    closest = list(distances.sort_values(ascending=True).head(2).index)
    standard_prediction = variable_df.loc[closest, 'maximum_nights_avg_bookings'].mean()
    standard_actual = variable_df.loc[ID_Z, 'maximum_nights_avg_bookings']
    prediction = un_standardise(standard_prediction, relevant['maximum_nights_avg_bookings'].mean(), relevant['maximum_nights_avg_bookings'].std())
    actual = un_standardise(standard_actual, relevant['maximum_nights_avg_bookings'].mean(), relevant['maximum_nights_avg_bookings'].std())
    prediction_text = "Prediction for {} {}".format(ID_Z, 'maximum_nights_avg_bookings')
    #actual_text = "Actual {} for {}".format(varZ, ID_Z)
    print(prediction_text, round(prediction,2))
    if prediction > 100:
        print('Investigation needed')
    else:
        print('Complies')
    #print(actual_text, round(actual,2))
    #standardised_Z_difference = standard_actual - standard_prediction   
    #Z_difference = actual - prediction
    #print("Error", round(Z_difference,2))
        


def prediction_func_Hosts(var1, var2, var3, ID_Z):
    def un_standardise(standardised_value, original_mean, original_std):
        return (standardised_value * original_std) + original_mean
    location_specific = data[data['neighbourhood_location'] == data.loc[ID_Z, 'neighbourhood_location']]
    location_numerical = data_tools.group_data(location_specific,'numerical')
    relevant = location_numerical[[var1, var2, var3, 'price_per_night_£']].dropna()
    standardised_relevant_data = (relevant - relevant.mean()) / relevant.std()
    variable_df = standardised_relevant_data
    row_Z = variable_df.loc[ID_Z, [var1, var2, var3]]
    variable_df.drop(ID_Z)
    def calculate_similarity(row):
        return distance.euclidean(row[[var1, var2, var3]], row_Z)
    distances = variable_df.head(1000).apply(calculate_similarity, axis=1)
    closest = list(distances.sort_values(ascending=True).head().index)
    standard_prediction = variable_df.loc[closest, 'price_per_night_£'].mean()
    standard_actual = variable_df.loc[ID_Z, 'price_per_night_£']
    prediction = un_standardise(standard_prediction, relevant['price_per_night_£'].mean(), relevant['price_per_night_£'].std())
    actual = un_standardise(standard_actual, relevant['price_per_night_£'].mean(), relevant['price_per_night_£'].std())
    prediction_text = "Suggested price per night for {} using the following listing charactetics {}, {}, {} = £ {}".format(ID_Z, var1, var2, var3, round(prediction,2))
    print(prediction_text)
    print("Your listings current price per night = £",round(actual,2))
    standardised_Z_difference = standard_actual - standard_prediction   
    Z_difference = actual - prediction
    print("Difference £", round(Z_difference,2))
    if Z_difference > 0:
        print('You should consider lowering your price')
    else:
        print('You should consider raising your price')