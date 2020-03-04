"""

This script reads zip code data produced by 01_vectorDataPreparations.py and creates a machine learning model for
predicting the number of unemployed people from zip code level population and spatial variables.

It assess the model accuracy with a test dataset but also predicts the number to all zip codes and writes it to a geopackage
for closer inspection

author: johannes.nyman@csc.fi
"""

import time
import geopandas as gpd
import pandas as pd
from math import sqrt
import os

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, BaggingRegressor,ExtraTreesRegressor, AdaBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error,r2_score

### FILL HERE the path where your data is. e.g "/scratch/project_2000599/students/26/data"
#base_folder = "/home/cscuser/gis-ml/data/paavo"
base_folder = "/Users/jnyman/Documents/local/rndm/ml_course_DEV/test"

### Relative path to the zip code geopackage file that was prepared by vectorDataPreparations.py
input_geopackage_path = os.path.join(base_folder,"zip_code_data_after_preparation.gpkg")

### Output file. Change name for different regression models
output_geopackage_path = os.path.join(base_folder,"median_income_per_zipcode_randomforest.gpkg")

### Just some pandas settings that allow us to print all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def trainAndEstimateModel(original_gdf):

    ### Split the gdf to x (the predictor attributes) and y (the attribute to be predicted)
    y = original_gdf['hr_mtu'] # Average income
    ### remove geometry and textual fields
    x = original_gdf.drop(['geometry','postinumer','nimi','hr_mtu'],axis=1)

    ### Split the both datasets to train (80%) and test (20%) datasets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=42)

    ### Choose the model to be used
    model = GradientBoostingRegressor(n_estimators=40, learning_rate=0.1,verbose=1)
    #model = RandomForestRegressor(n_estimators=40,verbose=1)
    #model = BaggingRegressor(n_estimators=40,verbose=1)
    #model = ExtraTreesRegressor(n_estimators=40,verbose=1)
    #model = AdaBoostRegressor(n_estimators=40)

    print(model)

    ### Train the model with x and y of the train dataset
    model.fit(x_train, y_train)
    
    ### Predict the unemployed number to the test dataset
    prediction = model.predict(x_test)

    ### Assess the accuracy of the model with root mean squared error, mean absolute error and coefficient of determination r2
    rmse = sqrt(mean_squared_error(y_test, prediction))
    mae = mean_absolute_error(y_test, prediction)
    r2 = r2_score(y_test, prediction)

    print("\nMODEL ACCURACY METRICS WITH TEST DATASET: \n" +
          "\t Root mean squared error: "+ str(rmse) + "\n" +
          "\t Mean absolute error: " + str(mae) + "\n" +
          "\t Coefficient of determination: "+ str(r2) + "\n")

    return model

def predictToAllZipCodes(model, original_gdf):

    ### Drop the not-used columns from original_gdf as done before model training.
    x = original_gdf.drop(['geometry','postinumer','nimi','hr_mtu'],axis=1)

    ### Predict the median income with already trained model
    prediction = model.predict(x)

    ### Join the predictions to the original geodataframe and pick only interesting columns for results
    original_gdf['predicted_hr_mtu'] = prediction.round(0)
    original_gdf['difference'] = original_gdf['predicted_hr_mtu'] - original_gdf['hr_mtu']
    resulting_gdf = original_gdf[['postinumer','nimi','hr_mtu','predicted_hr_mtu','difference','geometry']]

    return resulting_gdf


def main():
    ### Read the data into a geopandas dataframe named original_gdf
    original_gdf = gpd.read_file(input_geopackage_path)

    ### Build the model, train it and run it to the test part of the dataset
    model = trainAndEstimateModel(original_gdf)

    ### Predict the median income to all zip codes
    resulting_gdf = predictToAllZipCodes(model,original_gdf)

    ### Write resulting geodataframe to a geopackage
    resulting_gdf.to_file(output_geopackage_path,driver="GPKG")
    print("The predictions for all zip codes were written to: " + output_geopackage_path + "\n\nTHE END")


if __name__ == '__main__':
    ### This part just runs the main method and times it
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(round((end - start),0)) + " seconds")
