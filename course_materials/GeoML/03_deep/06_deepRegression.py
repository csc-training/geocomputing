"""

This script reads zip code data produced by vectorDataPreparations and creates a deep learning model for
predicting the median income from zip code level population and spatial variables.

It assess the model accuracy with a test dataset but also predicts the number to all zip codes and writes it to a geopackage
for closer inspection

author: johannes.nyman@csc.fi
"""

import time
import geopandas as gpd
from math import sqrt
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error,r2_score

import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import RMSprop


### FILL HERE the path to the data in Puhti
data_folder = "/scratch/project_2002044/data/GIS_ML_COURSE_DATA/data/paavo/"

### FILL HERE the path to YOUR working directory
results_folder = "/scratch/project_2002044/students/<YOUR-STUDENT-NUMBER>"

### Relative path to the zip code geopackage file that was prepared by vectorDataPreparations
input_geopackage_path = os.path.join(data_folder,"zip_code_data_after_preparation.gpkg")
output_geopackage_path = os.path.join(results_folder,"median_income_per_zipcode_deep_learning.gpkg")

def checkGPUavailability():
    device = tensorflow.test.is_gpu_available()
    if device:
        print("We have a GPU available!")
    else:
        print("Sadly no GPU available. :( you have settle with a CPU. Good luck!")


def trainAndEstimateModel(original_gdf):

    ### Split the gdf to x (the predictor attributes) and y (the attribute to be predicted)
    y = original_gdf['hr_mtu'].to_numpy()  # median income
    
    ### remove geometry, textual fields and the y field
    x = original_gdf.drop(['geometry', 'postinumer', 'nimi', 'hr_mtu'], axis=1).to_numpy()
    num_of_x_columns =  x.shape[1]

    ### Split the both datasets to train (80%) and test (20%) datasets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=42)

    ### Initialize a Sequential keras model
    model = Sequential()

    ### Add first layer with 64 perceptrons. Activation function is relu
    model.add(Dense(64, activation='relu', input_shape=(num_of_x_columns,)))

    ### Add another layer with 64 perceptrons
    model.add(Dense(64, activation='relu'))

    ### The last layer has to have only 1 perceptron as it is the output layer
    model.add(Dense(1))

    ### Setting optimizer and loss functions. Learning rate set to 0.001
    model.compile(optimizer=RMSprop(lr=.001), loss='mse', metrics=['mae','mse'])
    print(model.summary())

    ### Train the network with 1000 epochs and batch size of 64
    model.fit(x_train, y_train, epochs=1000, shuffle=True, batch_size=64, verbose=2)

    ### Evaluating the performance of the model using test data
    prediction = model.predict(x_test)
    r2 = r2_score(y_test, prediction)
    rmse = sqrt(mean_squared_error(y_test, prediction))
    mae = mean_absolute_error(y_test, prediction)

    print("\nMODEL ACCURACY METRICS WITH TEST DATASET: \n" +
          "\t Root mean squared error: "+ str(rmse) + "\n" +
          "\t Mean absolute error: " + str(mae) + "\n" +
          "\t Coefficient of determination: " + str(r2) + "\n")

    return model

def predictToAllZipCodes(model, original_gdf):
    ### Drop the not-used columns from original_gdf as done before model training.
    x = original_gdf.drop(['geometry', 'postinumer', 'nimi', 'hr_mtu'], axis=1).to_numpy()

    ### Predict the median income with the already trained model
    prediction = model.predict(x)

    ### Join the predictions to the original geodataframe and pick only interesting columns for results
    original_gdf['predicted_hr_mtu'] = prediction.round(0)
    original_gdf['difference'] = original_gdf['predicted_hr_mtu'] - original_gdf['hr_mtu']

    resulting_gdf = original_gdf[['postinumer','nimi','hr_mtu','predicted_hr_mtu','difference','geometry']]

    return resulting_gdf

def main():
    ### Let's test if we have a working GPU available (we don't)
    checkGPUavailability()

    ### Read the data into a geopandas dataframe named original_gdf
    original_gdf = gpd.read_file(input_geopackage_path,encoding='utf-8')

    ### Build the model, train it and run it to the test part of the dataset
    model = trainAndEstimateModel(original_gdf)

    ### Predict the median income to all zip codes
    resulting_gdf = predictToAllZipCodes(model,original_gdf)

    ### Write resulting geodataframe to a geopacakage
    resulting_gdf.to_file(output_geopackage_path, driver="GPKG")
    print("The predictions for all zip codes were written to: " + output_geopackage_path + "\n\nTHE END")


if __name__ == '__main__':
    ### This part just runs the main method and times it
    print("Script started!")
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(round((end - start),0)) + " seconds")
