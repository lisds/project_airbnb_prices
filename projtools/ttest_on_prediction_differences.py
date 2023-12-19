import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from scipy.spatial import distance
from projtools import data_tools
import seaborn as sns
from scipy.stats import norm
from scipy.stats import ttest_1samp

# Setup and preprocessing
data = data_tools.data_setup()
numerical_data = data_tools.group_data(data, 'numerical')

var1 = 'accommodates'
var2 = 'number_of_reviews'
var3 = 'host_listings_count'
varZ = 'price_per_night_£'
ID_X = 284532

cleaned_data = numerical_data.dropna(subset=[var1, var2, var3, varZ])
standardised_cleaned_data = (cleaned_data - cleaned_data.mean()) / cleaned_data.std()

# Linear regression model
X = standardised_cleaned_data[[var1, var2]]
Y = standardised_cleaned_data[var3]
model = LinearRegression().fit(X, Y)
a, b = model.coef_
c = model.intercept_

# Function to calculate z-coordinate on the plane and the error distance
def calculate_distance_to_plane(row, plane_coeffs):
    x, y, z_actual = row[var1], row[var2], row[var3]
    a, b, intercept = plane_coeffs
    z_on_plane = a * x + b * y + intercept
    error_distance_z = abs(z_actual - z_on_plane)
    return z_on_plane, error_distance_z




def find_closest_points(data, reference_row, num_points, plane_coeffs):
    # Calculate distances
    distances = data.apply(lambda row: calculate_distance_to_plane(row, plane_coeffs), axis=1)

    # Ensure distances are numeric
    distances_numeric = pd.to_numeric(distances, errors='coerce')

    # Return the n smallest distances
    return distances_numeric.nsmallest(num_points)


# Function to calculate average error and coordinate
def calculate_average_error_and_coordinate(closest_points, data, plane_coeffs):
    sum_z_on_plane = sum_error_distance = 0
    for index in closest_points.index:
        row = data.loc[index]
        z_on_plane, error_distance_z = calculate_distance_to_plane(row, plane_coeffs)
        sum_z_on_plane += z_on_plane
        sum_error_distance += error_distance_z
    num_points = len(closest_points)
    return sum_z_on_plane / num_points, sum_error_distance / num_points

# Function to predict point
def predict_point(average_z_on_plane, average_error, plane_coeffs):
    a, b, intercept = plane_coeffs
    # Normalize the normal vector to the plane
    normal_vector = np.array([a, b, -1])
    normalized_normal_vector = normal_vector / np.linalg.norm(normal_vector)
    # Movement vector in the z-direction
    movement_vector = normalized_normal_vector * average_error
    # Calculate the adjusted z-coordinate
    adjusted_z = average_z_on_plane + movement_vector[2]
    return adjusted_z


differences = []

# Loop through the first 10 rows
for index, row in cleaned_data.iloc[:5].iterrows():
    # Standardize the current row
    standardized_row = (row - cleaned_data.mean()) / cleaned_data.std()
    
    # Find the closest points
    closest_points = find_closest_points(standardised_cleaned_data, standardized_row, 5, (a, b, c))
    
    # Calculate average coordinate and error
    avg_z_on_plane, avg_error = calculate_average_error_and_coordinate(closest_points, standardised_cleaned_data, (a, b, c))
    
    # Predict new point
    predicted_z = predict_point(avg_z_on_plane, avg_error, (a, b, c))
    
    # Calculate difference
    actual_z = standardized_row[varZ]
    difference = actual_z - predicted_z
    differences.append(difference)


ind = cleaned_data.index
index = ind[:len(differences)]

differences_df = pd.DataFrame({
    'Difference': differences,
    'IDs': index
})
differences_df = differences_df.set_index('IDs')

print(differences_df.head())



plt.figure(figsize=(10, 6))
sns.histplot(differences, kde=True, color="blue", stat="density", linewidth=0)
plt.title("Normal Distribution of Differences")
plt.xlabel("Differences")
plt.ylabel("Density")

# Fitting the data to a normal distribution
mu, std = norm.fit(differences)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2, label=f"Fit: mu = {mu:.2f}, std = {std:.2f}")

plt.legend()
plt.show()

# for you specific property in question you can then test to see whether there is a large difference from the expected result 
# if there is you can test whether this result is significant or not 

# One-tailed hypothesis test for ID_X
ID_X_diff = differences_df.loc[ID_X]
population_mean = differences_df['Difference'].mean()

# create a hypothesis test to see if its significant 
# then run loads of them through the test to highlight the ones that could be dodgy 

#they will have a mean of zero no diffenece 
#error thats against the null hypothesis 
#is the mean ive observed compatbale 

# this will hopefully at the end run on 3 variables with you choice of variable to find out about in regard to a specific property 
# could have a think about what variables could suggest what 

#there is a difference in a null world 
#is id_X particularly strikign 
#look up help 

#provide ttest_1samp with differences

#what proportion of the data occurs above the reuslt in question 

