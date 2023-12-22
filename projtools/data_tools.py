# projtools/data_tools.py
import pandas as pd
from pathlib import Path
import numpy as np
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

    #Adding columns
    # Categorizing hosts by number of listings they have in London
    data['host_listings_group'] = pd.cut(data['calculated_host_listings_count'], 
                           bins=[0, 1, 10, 100, np.inf],
                           labels=['1 Property', '2-10 Properties', '11-100 Properties', '100+ Properties'])

    # Reordering columns
    data = data[[
        'host_id', 'host_name', 'host_since', 'host_location', 'host_about',
        'host_response_time', 'host_response_rate', 'host_acceptance_rate',
        'host_is_superhost', 'host_listings_group', 'host_listings_count',
        'host_lifetime_listings_count', 'host_verifications',
        'host_identity_verified', 'calculated_host_listings_count',
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

def Categorize_Host_Listings(host_listing_counts):
    """
    Categorize hosts by the unique number of listings they have.

    Parameters:
    - host_listing_counts: Series or DataFrame column containing the number of listings per host.

    Returns:
    - unique_host_listings_group: Series containing the categories for each host.
    """
    # Categorize hosts by the unique number of listings they have
    unique_host_listings_group = pd.cut(host_listing_counts, 
                                        bins=[0, 1, 10, 100, np.inf], 
                                        labels=['1 Property', '2-10 Properties', '11-100 Properties', '100+ Properties'])

    return unique_host_listings_group

def Add_host_group(data, host_listings_group):
    """
    Merge the data DataFrame with host groupings based on 'host_id' column.

    Parameters:
    - data: DataFrame containing your data.
    - host_listings_group: Series containing host groupings based on 'host_id'.

    Returns:
    - merged_data: DataFrame with the data merged with host groupings.
    """
    host_groupings_df = pd.DataFrame(host_listings_group)
    merged_data = pd.merge(data, host_groupings_df, left_on='host_id', right_index=True, how='left')
    
    # Rename the new column as 'host_group' and place it next to 'calculated_host_listings_count'
    merged_data = merged_data.rename(columns={'calculated_host_listings_count_x':'calculated_host_listings_count', 
                                              'calculated_host_listings_count_y':'host_listings_group'})

    merged_data = merged_data[['host_id', 'host_name', 'host_since', 'host_location', 'host_about',
                               'host_response_time', 'host_response_rate', 'host_acceptance_rate',
                               'host_is_superhost', 'host_listings_count', 'host_lifetime_listings_count',
                               'host_verifications', 'host_identity_verified',
                               'calculated_host_listings_count', 'host_listings_group',
                               'name', 'description', 'neighbourhood_location',
                               'neighbourhood_description', 'latitude', 'longitude', 'property_type', 'room_type',
                               'accommodates', 'bathrooms_text', 'bedrooms', 'beds', 'amenities', 'price_per_night_£',
                               'minimum_nights', 'maximum_nights', 'minimum_nights_avg_bookings', 'maximum_nights_avg_bookings', 'instant_bookable',
                               'number_of_reviews',
                               'review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness',
                               'review_scores_checkin', 'review_scores_communication', 'review_scores_location',
                               'review_scores_value', 'reviews_per_month', 'number_of_review_imgs', 'first_review', 'last_review']]
    return merged_data

def Add_long_term_rental(data):
    """
    Add a new column 'long_term_rental' to the DataFrame indicating whether a property
    is in breach of the 90-day limit.

    Parameters:
    - data: DataFrame containing your data.

    Returns:
    - data: DataFrame with the new column added.
    """
    # Create a boolean mask based on the 'maximum_nights_avg_bookings' column
    breach_90_day_limit = data['maximum_nights_avg_bookings'] > 90

    # Create a new column 'breach_90_day_limit' with True for breaches and False otherwise
    data['long_term_rental'] = breach_90_day_limit

    # Reorder the columns to place 'breach_90_day_limit' to the right of 'maximum_nights_avg_bookings'
    data = data[['host_id', 'host_name', 'host_since', 'host_location', 'host_about',
                               'host_response_time', 'host_response_rate', 'host_acceptance_rate',
                               'host_is_superhost', 'host_listings_count', 'host_lifetime_listings_count',
                               'host_verifications', 'host_identity_verified',
                               'calculated_host_listings_count', 'host_listings_group',
                               'name', 'description', 'neighbourhood_location',
                               'neighbourhood_description', 'latitude', 'longitude', 'property_type', 'room_type',
                               'accommodates', 'bathrooms_text', 'bedrooms', 'beds', 'amenities', 'price_per_night_£',
                               'minimum_nights', 'maximum_nights', 'minimum_nights_avg_bookings', 'maximum_nights_avg_bookings', 'long_term_rental', 'instant_bookable',
                               'number_of_reviews',
                               'review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness',
                               'review_scores_checkin', 'review_scores_communication', 'review_scores_location',
                               'review_scores_value', 'reviews_per_month', 'number_of_review_imgs', 'first_review', 'last_review']]

    return data