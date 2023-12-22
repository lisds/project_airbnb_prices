
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sps 
from projtools import data_tools
from scipy.spatial import distance
from projtools import k_best_neighbours_prediction
from projtools import quartile_prices

data = data_tools.data_setup()

long_term_listings = data[(data['maximum_nights_avg_bookings'] > 90) & (data['maximum_nights_avg_bookings'] < 1500)]

one_yr = long_term_listings[long_term_listings['maximum_nights_avg_bookings'] == 365]
one_yr_price_nights = one_yr[['price_per_night_£']]

three_yr = long_term_listings[long_term_listings['maximum_nights_avg_bookings'] == 1125]
three_yr_price_nights = three_yr[['price_per_night_£']]

one_year_mean = one_yr_price_nights['price_per_night_£'].mean() 

three_yr_mean = three_yr_price_nights['price_per_night_£'].mean() 

Q1_one = one_yr_price_nights['price_per_night_£'].quantile(0.25)
Q3_one = one_yr_price_nights['price_per_night_£'].quantile(0.75)

Q1_three = three_yr_price_nights['price_per_night_£'].quantile(0.25)
Q3_three = three_yr_price_nights['price_per_night_£'].quantile(0.75)


listings_around_one_year = long_term_listings[(long_term_listings['maximum_nights_avg_bookings'] > 330) & (long_term_listings['maximum_nights_avg_bookings'] < 400) & (long_term_listings['maximum_nights_avg_bookings'] != 365)]
listings_around_three_year = long_term_listings[(long_term_listings['maximum_nights_avg_bookings'] > 1090) & (long_term_listings['maximum_nights_avg_bookings'] < 1160) & (long_term_listings['maximum_nights_avg_bookings'] != 1125)]
 
around_one_mean = listings_around_one_year['price_per_night_£'].mean()
around_three_mean = listings_around_three_year['price_per_night_£'].mean()


Q3_around_one = listings_around_one_year['price_per_night_£'].quantile(0.75)
Q3_around_three = listings_around_three_year['price_per_night_£'].quantile(0.75)
