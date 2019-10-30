"""

This script reads zip code data produced by vectorDataPreparations.py and creates a machine learning model for
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

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error,r2_score
from sklearn.preprocessing import StandardScaler

### FILL HERE the path where your data is. e.g "/scratch/project_2000599/students/26/data"
base_folder = ""

### Relative path to the zip code geopackage file that was prepared by vectorDataPreparations.py
input_geopackage_path = os.path.join(base_folder,"zip_code_data_after_preparation.gpkg")
output_geopackage_path = os.path.join(base_folder,"num_unemployed_per_zipcode_deep_learning.gpkg")

### Just some pandas settings that allow us to print all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def readZipcodeData(zipcode_filepath):
    ### Read the data from a shapefile to a geopandas dataframe
    gdf = gpd.read_file(zipcode_filepath)
    print("\nTotal of " + str(len(gdf.index))+ " zip codes with " + str(len(gdf.columns)) + " columns")
    return gdf

def trainAndRunModel(original_gdf):

    ### Split the gdf to x (the predictor attributes) and y (the attribute to be predicted)
    y = original_gdf['pt_tyott'] # number of unemployed persons
    x = original_gdf.drop(['geometry','posti_alue','nimi','pt_tyott'],axis=1)

    ### Split the both datasets to train (80%) and test (20%) datasets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=63)

    ### Define the model to be used
    #model = GradientBoostingRegressor(n_estimators=40, learning_rate=0.1)
    model = RandomForestRegressor(n_estimators=40)

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

    ### Let's drop the not-needed columns from original_gdf
    x = original_gdf.drop(['geometry','posti_alue','nimi','pt_tyott'],axis=1)

    ### Predict number of unemployed people with already trained model
    prediction = model.predict(x)

    ### Join the predictions to the original geodataframe and pick only interesting columns for results
    original_gdf['predicted_pt_tyott'] = prediction.round(0)
    resulting_gdf = original_gdf[['posti_alue','nimi','pt_tyott','predicted_pt_tyott','geometry']]

    return resulting_gdf


def main():
    ### Read the data into a geopandas dataframe named original_gdf
    original_gdf = readZipcodeData(input_geopackage_path)

    ### Build the model, train it and run it to the test part of the dataset
    model = trainAndRunModel(original_gdf)

    ### Run the model to predict the number of unemployed people to all zip codes
    resulting_gdf = predictToAllZipCodes(model,original_gdf)

    ### Write resulting geodataframe to a geopackage
    resulting_gdf.to_file(output_geopackage_path,driver="GPKG")
    print("The predictions for all zip codes were written to: " + output_geopackage_path + "\n\nTHE END")


if __name__ == '__main__':
    ### This part just runs the main method and times it
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(round(((end - start) / 60),3)) + " minutes")
