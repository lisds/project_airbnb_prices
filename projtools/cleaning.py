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

    data_path = Path('../data/proj_data.csv')

    raw_data = pd.read_csv(data_path)

    data = raw_data.set_index('id')
    data = data.rename(columns={
        'neighborhood_overview': 'neighbourhood_description',
        'neighbourhood_cleansed': 'neighbourhood_location'
        
    })

    return data
