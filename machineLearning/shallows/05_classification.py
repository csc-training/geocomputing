#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This script reads forest stands and Sentinel 2A satellite data produced by raster_preparations_sentinel.sh and creates 4 a machine learning models for
predicting the forest main tree species from satellite data.

It assess the model accuracy with a test dataset but also predicts the main tree species for whole image (the cropped version).

author: kylli.ek@csc.fi
"""

import os, time
from imblearn.under_sampling import RandomUnderSampler
import numpy as np
import rasterio
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

#Set working directory and input/output file names.
#wrkFolder = r"\Temp\ML\exercises\classification"
wrkFolder = r"/scratch/project_2000599/classification"

# Input
inputImage =  os.path.join(wrkFolder,'T34VFM_20180829T100019_clipped_scaled.tif')
labelsImage =  os.path.join(wrkFolder,'forest_species_reclassified.tif')

# Outputs of 4 different models
RandomForestImage = os.path.join(wrkFolder,'T34VFM_20180829T100019_clipped_random_forest.tif')
SVCImage = os.path.join(wrkFolder,'T34VFM_20180829T100019_clipped_SVC.tif')
SGDImage = os.path.join(wrkFolder,'T34VFM_20180829T100019_clipped_SGD.tif')
GradientBoostImage = os.path.join(wrkFolder,'T34VFM_20180829T100019_clipped_gradient_boost.tif')
SVCImageGridSearch = os.path.join(wrkFolder,'T34VFM_20180829T100019_clipped_SVC_grid_search.tif')

# Available cores
n_jobs = 4

# Read data and shape it to suitable form for scikit-learn
# Exactly the same as for K-means for image data, labels part added
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

# Train the model and see how long it took.
def trainModel(x_train, y_train, clf):
    start_time = time.time()    
    # training the model
    clf.fit(x_train, y_train)
    print('Model training took: ', round((time.time() - start_time), 2), ' seconds')
    return clf

# Predict on test data and see the model accuracy
def estimateModel(clf, x_test, y_test):
    test_predictions = clf.predict(x_test)
    print('Confusion matrix: \n', confusion_matrix(y_test, test_predictions))
    print('Classification report: \n', classification_report(y_test, test_predictions))

# Predict on whole image and save it as .tif file
def predictImage(trained_model, predictedImagePath):
	# Read the satellite image
    with rasterio.open(inputImage, 'r') as image_dataset:
        start_time = time.time()    
        
		#Reshape data to 1D as we did before model training
        image_data = image_dataset.read()
        image_data2 = np.transpose(image_data, (1, 2, 0))
        pixels = image_data2.reshape(-1, 3)
        
        # predicting the classification
        prediction = trained_model.predict(pixels)
        
		# Reshape back to 2D
        print('Prediction shape in 1D: ', prediction.shape)
        prediction2D = np.reshape(prediction, (image_dataset.meta['height'], image_dataset.meta['width']))
        print('Prediction shape in 2D: ', prediction2D.shape)
		
		# Save the results as .tif file.
		# Copy the coorindate system information, image size and other metadata from the satellite image 
        outputMeta = image_dataset.meta
		# Change the number of bands and data type.
        outputMeta.update(count=1, dtype='uint8')
        # Writing the image on the disk
        with rasterio.open(predictedImagePath, 'w', **outputMeta) as dst:
            dst.write(prediction2D, 1)
        
        print('Predicting took: ', round((time.time() - start_time), 1), ' seconds')


def main():
    # Read the input datasets with Rasterio
    labels_dataset = rasterio.open(labelsImage)
    image_dataset = rasterio.open(inputImage)  
    
	# Prepare data for all the models
    input_image, input_labels = prepareData(image_dataset, labels_dataset)
	# Divide the data to test and training datasets
    x_train, x_test, y_train, y_test = train_test_split(input_image, input_labels, test_size=0.2, random_state=63)
    
	# SVM can not handle well big amounts of training data, so use only small 
    # part of the data (5 %)    
    # Take random 5 % sample of the data
    sp = StratifiedShuffleSplit(n_splits=1, test_size=0.95, random_state=63)
    for train_index, _ in sp.split(input_image, input_labels):
        input_image2, input_labels2 = input_image[train_index], input_labels[train_index]
    print ('Dataframe after downsampling for SVM, shape 2D: ', input_image2.shape) 
    # Divide this smaller sample to test and training datasets
    x_train2, x_test2, y_train2, y_test2 = train_test_split(input_image2, input_labels2, test_size=0.2, random_state=63)	

    # Fit and predict 4 models on the data. Each outputs a .tif image with the predicted classification.
	# The workflow is the same for all, except for SVM where smaller sample of data is used.
	
    print("Random forest")
    # Initialize the random forest classifier and give the hyperparameters.
    clf_random_forest = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=0, n_jobs=n_jobs)
    random_forest_model = trainModel(x_train, y_train, clf_random_forest)	
    estimateModel(random_forest_model, x_test, y_test)
    predictImage(random_forest_model, RandomForestImage)
    print('Feature importances: \n', random_forest_model.feature_importances_)

    print("Stochastic Gradient Decent")
    clf_SGD = SGDClassifier(alpha=0.000001, loss="log", learning_rate='adaptive', eta0=.1, n_jobs=n_jobs, max_iter=100)
    SGD_model = trainModel(input_image, input_labels, clf_SGD)
    estimateModel(SGD_model, x_test, y_test)
    predictImage(SGD_model, SGDImage)
    
    print("Gradient Boost")
    clf_gradient_boost = GradientBoostingClassifier(n_estimators=50, learning_rate=.05)
    gradient_boost_model = trainModel(input_image, input_labels, clf_gradient_boost)
    estimateModel(gradient_boost_model, x_test, y_test)
    predictImage(gradient_boost_model, GradientBoostImage)
    print('Feature importances: \n', gradient_boost_model.feature_importances_)    

    print("Support Vector Classifier")   
    clf_svc = SVC(kernel='rbf', gamma='auto')
    svc_model = trainModel(x_train2, y_train2, clf_svc)
    estimateModel(svc_model, x_test2, y_test2)
    predictImage(svc_model, SVCImage)
                      
					 
					  
    print('Grid search for SVC')
	# Find the optimal parameters for SVM
    param_grid = {'C': [1000, 10000], 'gamma': [1, 10]}
    # Initialize the grid search, cv is the number of iterations, kept at minimum here for faster results.
    grid = GridSearchCV(SVC(), param_grid, verbose=1, n_jobs=n_jobs, cv=2)
    # Try different options
    grid.fit(x_train2, y_train2)
	# Plot the best
    print('Best selected parameters: ',format(grid.best_params_))
    print('Best estimator: ',format(grid.best_estimator_))
    # Test the classifier using test data
    estimateModel(grid, x_test2, y_test2)
	# Save the results as .tif
    predictImage(grid, SVCImageGridSearch)
 

if __name__ == '__main__':
    main()