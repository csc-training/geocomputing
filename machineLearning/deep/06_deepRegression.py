"""

This script reads zip code data produced by vectorDataPreparations.py and creates a deep learning model for
predicting the number of unemployed people from zip code level population and spatial variables.

It assess the model accuracy with a test dataset but also predicts the number to all zip codes and writes it to a geopackage
for closer inspection

author: johannes.nyman@csc.fi
"""

import time
import geopandas as gpd
from math import sqrt
import os
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import RMSprop

### FILL HERE the path where your data is. e.g "/scratch/project_2000599/students/26/data"
base_folder = ""

### Relative path to the zip code geopackage file that was prepared by vectorDataPreparations.py
input_geopackage_path = os.path.join(base_folder,"zip_code_data_after_preparation.gpkg")
output_geopackage_path = os.path.join(base_folder,"num_unemployed_per_zipcode_deep_learning.gpkg")

def trainAndEstimateModel(original_gdf):
    ### Split the gdf to x (the predictor attributes) and y (the attribute to be predicted)
    y = original_gdf['pt_tyott'].to_numpy()  # number of unemployed persons
    ### remove geometry and textual fields
    x = original_gdf.drop(['geometry', 'posti_alue', 'nimi', 'pt_tyott'], axis=1).to_numpy()

    ### Split the both datasets to train (80%) and test (20%) datasets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=63)

    ### Initialize a Sequential keras model
    model = Sequential()
    # add first layer with 64 perceptrons. 121 in input_shape goes for the number of attributes used in training
    model.add(Dense(64, activation='relu', input_shape=(121,)))
    model.add(Dropout(0.2))
    # add second layer with 32 perceptrons
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.2))    
    # add third layer with 16 perceptrons
    model.add(Dense(16, activation='relu'))
    model.add(Dropout(0.2))    
    # adding a linear layer with no activation functions since this is a regressor model
    model.add(Dense(1))
    # setting optimizer and loss functions. learning rate set to 0.01
    model.compile(optimizer=RMSprop(lr=.01), loss='mse', metrics=['mae'])
    # train the network in 100 epoch
    model.fit(x_train, y_train, epochs=100, batch_size=32)
    # evaluating the performance of the model using test data
    mse, mae = model.evaluate(x_test, y_test)
    rmse = sqrt(mse)

    print("\nMODEL ACCURACY METRICS WITH TEST DATASET: \n" +
          "\t Root mean squared error: "+ str(rmse) + "\n" +
          "\t Mean absolute error: " + str(mae) + "\n")

    return model

def predictToAllZipCodes(network, original_gdf):
    ### Drop the not-used columns from original_gdf as done before model training.
    x = original_gdf.drop(['geometry', 'posti_alue', 'nimi', 'pt_tyott'], axis=1).to_numpy()

    ### Predict number of unemployed people with the already trained model
    prediction = network.predict(x)

    ### Join the predictions to the original geodataframe and pick only interesting columns for results
    original_gdf['predicted_pt_tyott'] = prediction.round(0)
    resulting_gdf = original_gdf[['posti_alue','nimi','pt_tyott','predicted_pt_tyott','geometry']]

    return resulting_gdf

def main():
    ### Read the data into a geopandas dataframe named original_gdf
    original_gdf = gpd.read_file(input_geopackage_path,encoding='utf-8')

    ### Build the model, train it and run it to the test part of the dataset
    model = trainAndEstimateModel(original_gdf)

    ### Predict the number of unemployed people to all zip codes
    resulting_gdf = predictToAllZipCodes(model,original_gdf)

    ### Write resulting geodataframe to a geopacakage
    resulting_gdf.to_file(output_geopackage_path, driver="GPKG")
    print("The predictions for all zip codes were written to: " + output_geopackage_path + "\n\nTHE END")


if __name__ == '__main__':
    ### This part just runs the main method and times it
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(round((end - start),0)) + " seconds")
