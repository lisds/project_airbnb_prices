# projtools/data_setup.py

import pandas as pd
from pathlib import Path

def data_setup():
    """
    Load and clean the project data.

    Reads the project data from the CSV file, sets the 'id' column as the index,
    and renames columns for better clarity.

    Returns:
    --------
    pd.DataFrame
        Cleaned and processed DataFrame.
    """
    
    #Setting path to data
    data_path = Path('../data/proj_data.csv')

    #Creating Pandas df
    raw_data = pd.read_csv(data_path)

    #Setting the index
    data = raw_data.set_index('id')
    
    #Renaming columns
    data = data.rename(columns={
        'neighborhood_overview': 'neighbourhood_description',
        'neighbourhood_cleansed': 'neighbourhood_location'
        
    })

    #Dropping unecessary columns
    data = data.drop(columns=['listing_url','host_picture_url', 'host_url'])
   
    return data
