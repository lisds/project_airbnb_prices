import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
from scipy.spatial import distance
from projtools import data_tools

def analyze_data(var1, var2, var3, varZ, ID_Z):
    # Data setup
    data = data_tools.data_setup()
    numerical_data = data_tools.group_data(data, 'numerical')

    # Cleaning and standardizing data
    cleaned_data = numerical_data.dropna(subset=[var1, var2, var3, varZ])
    standardised_cleaned_data = (cleaned_data - cleaned_data.mean()) / cleaned_data.std()

    # Linear regression
    X = standardised_cleaned_data[[var1, var2]]
    Y = standardised_cleaned_data[var3]
    model = LinearRegression().fit(X, Y)
    a, b = model.coef_
    c = model.intercept_

    # 3D plot setup
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plotting data points
    x1 = standardised_cleaned_data[var1]
    y1 = standardised_cleaned_data[var2]
    z1 = standardised_cleaned_data[var3]
    ax.scatter(x1, y1, z1, color='blue', label='Data Points')

    # Plane of best fit
    x2, y2 = np.meshgrid(np.linspace(x1.min(), x1.max(), 10), np.linspace(y1.min(), y1.max(), 10))
    z2 = a * x2 + b * y2 + c
    ax.plot_surface(x2, y2, z2, alpha=0.5, rstride=100, cstride=100, color='red', label='Best Fit Plane')
    ax.set_xlabel(var1)
    ax.set_ylabel(var2)
    ax.set_zlabel(var3)
    ax.legend()
    plt.show()

    # Finding closest points
    Row_Z_variables = standardised_cleaned_data.loc[ID_Z, [var1, var2, var3]]
    distances = standardised_cleaned_data.apply(lambda row: distance.euclidean(row[[var1, var2, var3]], Row_Z_variables), axis=1)
    top_5_closest = distances.nsmallest(5)
    comparison_IDs = np.array(top_5_closest.index)
    comparison_rows = standardised_cleaned_data.loc[comparison_IDs]
    results_for_varZ = comparison_rows[varZ]

    # Analysis of closest points
    coordinates = [(value, value, value) for value in results_for_varZ]
    sum_z_on_plane = sum_error_distance = 0
    for coord in coordinates:
        x, y, z_actual = coord
        z_on_plane = a * x + b * y + c
        error_distance_z = abs(z_actual - z_on_plane)
        sum_z_on_plane += z_on_plane
        sum_error_distance += error_distance_z
    
    # Average calculations
    average_z_on_plane = sum_z_on_plane / len(coordinates)
    average_error_distance = sum_error_distance / len(coordinates)
    z_av_coordinates = np.array([average_z_on_plane, average_z_on_plane, average_z_on_plane])
    normal_vector = np.array([a, b, -1])
    normalized_normal_vector = normal_vector / np.linalg.norm(normal_vector)
    movement_vector = normalized_normal_vector * average_error_distance
    new_point = z_av_coordinates + movement_vector

    standardised_prediction = np.mean(new_point)

    # Reverse standardization for the predicted value
    varZ_mean = cleaned_data[varZ].mean()
    varZ_std = cleaned_data[varZ].std()

    # Applying the reverse standardization formula
    prediction = standardised_prediction * varZ_std + varZ_mean

    # Results
    print("Standardised Actual", standardised_cleaned_data.loc[ID_Z, varZ])
    print("Standardised Prediction", standardised_prediction)

    print("Actual", data.loc[ID_Z, varZ] )
    print("Prediction", prediction)

# Example usage of the function
    
analyze_data('accommodates', 'number_of_reviews', 'host_listings_count', 'price_per_night_£', 106332)

 