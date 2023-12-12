# projtools/data_setup.py

import pandas as pd
from pathlib import Path

def data_setup():
    """
    Load and clean the project data.

    Reads the project data from the CSV file, sets the 'id' column as the index,
    removes the '$' from the 'price' column, renames columns for better clarity,
    and drops unnecessary columns.

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

    # Removing '$' from the 'price' column
    data['price'] = data['price'].str.replace('$', '')
    
    # Renaming columns
    data = data.rename(columns={
        'neighborhood_overview': 'neighbourhood_description',
        'neighbourhood_cleansed': 'neighbourhood_location',
        'price': 'price_per_night_$',
        'host_total_listings_count':'host_lifetime_listings_count',
        'minimum_nights_avg_ntm':'minimum_nights_avg_bookings',
        'maximum_nights_avg_ntm':'maximum_nights_avg_bookings',
        'number_of_reviews_ltm':'number_of_review_imgs'
    })

    # Dropping unnecessary columns
    data = data.drop(columns=['listing_url', 'host_picture_url', 'host_url'])
   
    return data


def group_data(data):
    """
    Group the data into different categories.

    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame containing the project data.

    Returns:
    --------
    Dataframe tuple
        A tuple containing DataFrames for host data, property data, review data, and location data.
    """

    host_data = data[['host_id', 'host_name', 'host_since', 'host_location', 'host_about', 'host_response_rate',
                      'host_response_rate', 'host_acceptance_rate', 'host_is_superhost', 'host_listings_count',
                      'host_lifetime_listings_count', 'host_verifications', 'host_identity_verified',
                      'calculated_host_listings_count', 'calculated_host_listings_count_entire_homes',
                      'calculated_host_listings_count_private_rooms', 'calculated_host_listings_count_shared_rooms']]

    property_data = data[['name', 'description', 'property_type', 'room_type', 'accommodates', 'bathrooms_text',
                          'bedrooms', 'beds', 'amenities', 'price_per_night_$', 'minimum_nights', 'maximum_nights',
                          'minimum_nights_avg_bookings', 'maximum_nights_avg_bookings', 'instant_bookable']]

    review_data = data[['review_scores_rating', 'number_of_reviews', 'review_scores_accuracy',
                        'review_scores_cleanliness', 'review_scores_checkin', 'review_scores_communication',
                        'review_scores_location', 'review_scores_value', 'reviews_per_month',
                        'number_of_review_imgs', 'first_review', 'last_review']]

    location_data = data[['neighbourhood_location', 'neighbourhood_description', 'latitude', 'longitude']]

    return host_data.head, property_data, review_data, location_data
