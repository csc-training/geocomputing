#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This script reads forest stands and Sentinel 2A satellite data produced by raster_preparations_sentinel.sh and creates fully connected deep learning model for
predicting the forest main tree species from satellite data.

It assess the model accuracy with a test dataset but also predicts the main tree species for whole image (the cropped version).

author: ziya.yektay@csc.fi, kylli.ek@csc.fi
"""

import os, time
from imblearn.under_sampling import RandomUnderSampler
import numpy as np
import rasterio
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from tensorflow.keras import models, layers
from tensorflow.keras import optimizers
from tensorflow.keras.models import model_from_json
from tensorflow.keras.utils import to_categorical


#Set working directory and input/output file names.

data_folder = "/scratch/project_2002044/data/GIS_ML_COURSE_DATA/data/forest"

results_folder = "/scratch/project_2002044/students/<YOUR-STUDENT-NUMBER>"

# Input
inputImage =  os.path.join(data_folder,'T34VFM_20180829T100019_clipped_scaled.tif')
labelsImage =  os.path.join(data_folder,'forest_species_reclassified.tif')

# Outputs of the model
# Saved model and its weights
fullyConnectedModel = os.path.join(results_folder,'fullyConnectedModel_forest.json')
fullyConnectedWeights = os.path.join(results_folder,'fullyConnectedWeights_forest.h5')
# Predicted .tif image
fullyConnectedImageCropped = os.path.join(results_folder,'T34VFM_20180829T100019_clipped_fullyConnected.tif')

# Read data and shape it to suitable form for keras.
# (Exactly the same as for scikit-learn classification.)
def prepareData(image_dataset, labels_dataset):    
    # Read the pixel values from .tif file as dataframe
    image_data = image_dataset.read()

    # We have to change the data format from bands x width x height to width*height x bands
    # This means that each pixel from the original dataset has own row in the result dataframe.
    # Check shape of input data
    print ('Dataframe original shape, 3D: ', image_data.shape)    
    # First move the bands to last axis.
    image_data2 = np.transpose(image_data, (1, 2, 0))
    # Check again the data shape, now the bands should be last.
    print ('Dataframe shape after transpose, 3D: ', image_data2.shape) 
    
    # Then reshape to 1D.
    pixels = image_data2.reshape(-1, 3)
    print ('Dataframe shape after transpose and reshape, 2D: ', pixels.shape) 
    
	# For labels only reshape to 1D is enough.
    labels_data = labels_dataset.read()
    input_labels = labels_data.reshape(-1)
    print ('Labels shape after reshape, 1D: ', pixels.shape)
    
    # The forest classes are very imbalanced in the dataset, so undersample the majority classes
    rus = RandomUnderSampler(random_state=63)
    pixels_resampled, labels_resampled = rus.fit_resample(pixels, input_labels)   
    print ('Dataframe shape after undersampling of majority classes, 2D: ', pixels_resampled.shape)

    return pixels_resampled, labels_resampled

# Train the fully connected model and save it.
def trainModel(x_train, y_train):
    start_time = time.time()    

    # Initializing a sequential model
    model = models.Sequential()
    # adding the first layer containing 64 perceptrons. 3 is representing the number of bands used for training
    model.add(layers.Dense(64, activation='relu', input_shape=(3,)))
    # add the first dropout layer
    model.add(layers.Dropout(rate=0.2))
    # adding more layers to the model
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dropout(rate=0.2))
    model.add(layers.Dense(16, activation='relu'))
    # adding the output layer to the model, note:
	# - the activation is 'softmax', should be used for multi-class classification models
	# - size=4, for 4 classes
    model.add(layers.Dense(4, activation='softmax'))
    
	# Compile the model, using:
	# - Adam optimizer, often used, but could be some other optimizer too.
	# -- learning_rate is 0.001
	# - categorical_crossentropy loss function (should be used with multi-class classification)
    model.compile(optimizer=optimizers.Adam(learning_rate=0.01), loss='categorical_crossentropy', metrics=['accuracy'])
    
	# Encode the labels categorically (as we did with the region names in Postcode preparations)
	# As result each pixel has a label, which is a 1D vector with 4 elements, each representing the probability of belonging to each class
    y_train_categorical = to_categorical(y_train)

    # Train the model
    model.fit(x_train, y_train_categorical, epochs=2, batch_size=128, verbose=2)	
	
    # Save the model to disk
    # Serialize the model to JSON
    model_json = model.to_json()
    with open(fullyConnectedModel, "w") as json_file:
        json_file.write(model_json)
    # Serialize weights to HDF5
    model.save_weights(fullyConnectedWeights)
    print('Saved model to disk:  \nModel: ', fullyConnectedModel, '\nWeights: ',  fullyConnectedWeights)
    print('Model training took: ', round((time.time() - start_time), 0), ' seconds')
    return model

# Predict on test data and see the model accuracy
def estimateModel(trained_model, x_test, y_test):
    
	# Encode the test data labels
    y_test_categorical = to_categorical(y_test)
	
    # Evaluate the performance of the model by the data, it has never seen
	# verbose=0 avoids printing to output a lot of unclear text (good in Puhti)
    test_loss, test_acc = trained_model.evaluate(x_test, y_test_categorical, verbose=0)
    print('Test accuracy:', test_acc)
    
	# Calculate confusion matrix and classification report as we did with shallow classifier.
	# Use scikit-learn functions for that.
	# First predict for the x_test
    test_prediction = trained_model.predict(x_test)	
	# The model returns a 2D array, with:
	# - each row representing one pixel.
	# - each column representing the probablity of this pixel representing each category	
    print ('Test prediction dataframe shape, original 2D: ', test_prediction.shape) 	
	
	# Find which class was most likely for each pixel and select only that class for the output.
	# Output is 1D array, with the most likely class index given for each pixel.
	# Argmax returns the indices of the maximum values 
    predicted_classes = np.argmax(test_prediction,axis=1)
    print ('Test prediction dataframe shape, after argmax, 1D: ', predicted_classes.shape) 	

    print('Confusion matrix: \n', confusion_matrix(y_test, predicted_classes))
    print('Classification report: \n', classification_report(y_test, predicted_classes))	


# Predict on whole image and save it as .tif file
# Otherwise exactly the same as with shallow classifiers, but:
# - Load the model from a file.
# - argmax is used for the prediction results.
# - Data type is changed to in8, keras returns int64, which GDAL does not support.
def predictImage(predictedImagePath, predictImage):
    # Load json and create model
    json_file = open(fullyConnectedModel, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # Load weights into new model
    loaded_model.load_weights(fullyConnectedWeights)
    print("Loaded model from disk")
	
    # Read the satellite image
    with rasterio.open(predictImage, 'r') as image_dataset:
        start_time = time.time()    
        
        #Reshape data to 1D as we did before model training
        image_data = image_dataset.read()
        image_data2 = np.transpose(image_data, (1, 2, 0))
        pixels = image_data2.reshape(-1, 3)
        
        # Predict for all pixels
        prediction = loaded_model.predict(pixels)
        print ('Prediction dataframe shape, original 2D: ', prediction.shape) 	
		# Find the most likely class for each pixel.
        predicted_classes = np.argmax(prediction,axis=1)
        print ('Prediction dataframe shape, after argmax, 1D: ', predicted_classes.shape) 	
		  
        # Reshape back to 2D as in original raster image
        prediction2D = np.reshape(predicted_classes, (image_dataset.meta['height'], image_dataset.meta['width']))
        print('Prediction shape in 2D: ', prediction2D.shape)
		
		# Change data type to int8
        predicted2D_int8 = np.int8(prediction2D)
		
		# Save the results as .tif file.
		# Copy the coordinate system information, image size and other metadata from the satellite image 
        outputMeta = image_dataset.meta
		# Change the number of bands and data type.
        outputMeta.update(count=1, dtype='int8')
        # Writing the image on the disk
        with rasterio.open(predictedImagePath, 'w', **outputMeta) as dst:
            dst.write(predicted2D_int8, 1)
        
        print('Predicting took: ', round((time.time() - start_time), 0), ' seconds')


def main():
    # Read the input datasets with Rasterio
    labels_dataset = rasterio.open(labelsImage)
    image_dataset = rasterio.open(inputImage)  
    
	# Prepare data for the model
    input_image, input_labels = prepareData(image_dataset, labels_dataset)
	# Divide the data to test and training datasets
    x_train, x_test, y_train, y_test = train_test_split(input_image, input_labels, test_size=0.2, random_state=63)
    

    # Fit and predict the fully connected deep learning model on the data. Outputs a .tif image with the predicted classification.	
    print("FullyConnected")
    fullyConnectedModel = trainModel(x_train, y_train)	
    estimateModel(fullyConnectedModel, x_test, y_test)
    predictImage(fullyConnectedImageCropped, inputImage)
                      
if __name__ == '__main__':
    ### This part just runs the main method and times it
    print("Script started!")
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(round((end - start),0)) + " seconds")
