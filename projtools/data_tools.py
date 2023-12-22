# projtools/data_tools.py
import pandas as pd
from pathlib import Path
import numpy as np
pd.set_option('display.max_columns', None)


def data_setup():
    """
    Load and clean the project data.

    Reads the project data from the CSV file
    Sets the 'id' column as the index,
    Removes '\$,' from the 'price' column
    Converts from dollars to pounds for the time period of the dataset
    Converts NaN values in bedrooms to 0 for studios
    Renames columns for better clarity,
    Drops unnecessary columns.
    Reorders the columns to group related information together.

    Returns:
    --------
    pd.DataFrame
        Cleaned and processed DataFrame.
    """
    
    # Setting path to data
    data_path = Path('../data/proj_data.csv')

    # Creating Pandas df
    raw_data = pd.read_csv(data_path)

    # Setting the index
    data = raw_data.set_index('id')

    # Cleaning 'price' column and converting to a float
    data['price'] = data['price'].replace('[\$,]', '', regex=True).astype(float)

    #Converting the price from dollars to pounds using the exchange rate from September 2022  {cite}'exchangeratesuk_2022'
    data['price'] = data['price'] * 0.9348

    #Converting NaN Values to 0
    data['bedrooms'] = data['bedrooms'].fillna(0)
    
    # Renaming columns
    data = data.rename(columns={
        'neighborhood_overview': 'neighbourhood_description',
        'neighbourhood_cleansed': 'neighbourhood_location',
        'price': 'price_per_night_£',
        'host_total_listings_count': 'host_lifetime_listings_count',
        'minimum_nights_avg_ntm': 'minimum_nights_avg_bookings',
        'maximum_nights_avg_ntm': 'maximum_nights_avg_bookings',
        'number_of_reviews_ltm': 'number_of_review_imgs'
    })

    # Dropping unnecessary columns
    data = data.drop(columns=['listing_url', 'host_picture_url', 'host_url'])

    #Adding column
    # Categorizing hosts by number of listings they have in London
    # Calculate the total number of distinct listings for each host
    host_listing_counts = data.groupby('host_id')['calculated_host_listings_count'].first()

    # Categorize hosts based on the unique number of listings
    host_listings_group = pd.cut(host_listing_counts, 
                                    bins=[0, 1, 10, 100, np.inf], 
                                    labels=['1 Property', '2-10 Properties', '11-100 Properties', '100+ Properties'])

    # Create a new column
    data['host_listings_group'] = host_listings_group


    # Reordering columns
    data = data[[
        'host_id', 'host_name', 'host_since', 'host_location', 'host_about',
        'host_response_time', 'host_response_rate', 'host_acceptance_rate',
        'host_is_superhost', 'host_listings_group', 'host_listings_count',
        'host_lifetime_listings_count', 'host_verifications',
        'host_identity_verified', 'calculated_host_listings_count', 'host_listings_group',
        'calculated_host_listings_count_entire_homes',
        'calculated_host_listings_count_private_rooms',
        'calculated_host_listings_count_shared_rooms',
        'name', 'description', 'neighbourhood_location',
        'neighbourhood_description', 'latitude', 'longitude', 'property_type', 'room_type',
        'accommodates', 'bathrooms_text', 'bedrooms', 'beds', 'amenities', 'price_per_night_£',
        'minimum_nights', 'maximum_nights', 'minimum_nights_avg_bookings', 'maximum_nights_avg_bookings', 'instant_bookable',
        'number_of_reviews',
        'review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness',
        'review_scores_checkin', 'review_scores_communication', 'review_scores_location',
        'review_scores_value', 'reviews_per_month', 'number_of_review_imgs', 'first_review', 'last_review',
    ]]
   
    return data


def group_data(data, data_type):
    """
    Group the data into different categories.

    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame containing the project data.
    data_type : str
        The type of data to retrieve ('host', 'property', 'review', 'location', 'numerical').

    Returns:
    --------
    pd.DataFrame
        The requested DataFrame.
    """

    if data_type == 'host':
        return data[['host_id', 'host_name', 'host_since', 'host_location', 'host_about', 'host_response_rate',
                     'host_response_rate', 'host_acceptance_rate', 'host_is_superhost', 'host_listings_count',
                     'host_lifetime_listings_count', 'host_verifications', 'host_identity_verified',
                     'calculated_host_listings_count', 'calculated_host_listings_count_entire_homes',
                     'calculated_host_listings_count_private_rooms', 'calculated_host_listings_count_shared_rooms']]
    elif data_type == 'property':
        return data[['name', 'description', 'property_type', 'room_type', 'accommodates', 'bathrooms_text',
                      'bedrooms', 'beds', 'amenities', 'price_per_night_£', 'minimum_nights', 'maximum_nights',
                      'minimum_nights_avg_bookings', 'maximum_nights_avg_bookings', 'instant_bookable']]
    elif data_type == 'review':
        return data[['review_scores_rating', 'number_of_reviews', 'review_scores_accuracy',
                      'review_scores_cleanliness', 'review_scores_checkin', 'review_scores_communication',
                      'review_scores_location', 'review_scores_value', 'reviews_per_month',
                      'number_of_review_imgs', 'first_review', 'last_review']]
    elif data_type == 'location':
        return data[['neighbourhood_location', 'neighbourhood_description', 'latitude', 'longitude']]
    elif data_type == 'numerical':
        return data[['host_listings_count', 'host_lifetime_listings_count', 'calculated_host_listings_count', 
                      'calculated_host_listings_count_entire_homes', 'calculated_host_listings_count_private_rooms', 'price_per_night_£',  
                      'accommodates', 'bedrooms', 'beds', 'minimum_nights', 'maximum_nights', 'minimum_nights_avg_bookings', 
                      'maximum_nights_avg_bookings', 'number_of_reviews', 'review_scores_rating', 'review_scores_accuracy', 
                      'review_scores_cleanliness', 'review_scores_checkin', 'review_scores_communication', 'review_scores_communication', 
                      'review_scores_location', 'review_scores_value', 'reviews_per_month', 'number_of_review_imgs']]
    else:
        raise ValueError("Invalid data_type. Choose from 'host', 'property', 'review', 'location', or 'numerical'.")


def Top_5_values(dataframe, column_name):
    """
    Return the top 5 most frequent values from the specified column in the given dataframe.

    Args:
    dataframe (pandas.DataFrame): The dataframe containing the data.
    column_name (str): The name of the column to analyze for frequency.

    Returns:
    pandas.Series: A series with the top 5 values and their counts.
    """
    return dataframe[column_name].value_counts().head(5)

