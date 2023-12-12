# Importing relevant modules
import pandas as pd
from pathlib import Path

#Memory optimisation for large data sets
pd.set_option('mode.copy_on_write', True)

#Set Path to Data
data_path = Path(__file__).resolve().parents[1] / 'data' / 'proj_data.csv'

#Set Data Variable to pandas df of data file
data = pd.read_csv(data_path)

#Cleaning
#Setting index to the ID column
data = data.set_index('id')

print(data)