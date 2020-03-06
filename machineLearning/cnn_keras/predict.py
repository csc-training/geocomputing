# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 12:46:58 2020

@author: ekkylli
"""
import os, time
import numpy as np
import rasterio
from tensorflow.keras.models import load_model

data_dir='/scratch/project_2002044/test/johannes/tiles'
#data_dir='C:\\temp\\ML_course_data\\tiles'
results_dir='/scratch/project_2002044/test/kylli'

# Folders with data and model
prediction_data_dir = os.path.join(data_dir, 'image_prediction_tiles_512') 
test_tiles_file = os.path.join(data_dir, 'test_tiles.csv')

model_final = os.path.join(results_dir, 'model_final.h5')

# Folders for results and log
predicted_dir = os.path.join(results_dir, 'predicted_tiles')

# Predict on whole image and save it as .tif file
def predictImage(model, dataImage):
    dataForPredictionFile = os.path.join(prediction_data_dir, dataImage)
	# Read the satellite image
    predictedImageFile = os.path.join(predicted_dir, dataImage)
    with rasterio.open(dataForPredictionFile, 'r') as image_dataset:
        start_time = time.time()    
        
		#Reshape data to 1D as we did before model training
        image_data = image_dataset.read()
        image_data2 = np.transpose(image_data, (1, 2, 0))  
        image_data3 = image_data2.reshape(1, 512, 512, 3)
        
        # predicting the class for each pixel
        prediction = model.predict(image_data3)
        
		# Reshape back to 2D
        print('Prediction shape: ', prediction.shape)
        prediction2 = prediction.reshape(512, 512, 1)
        print('Prediction shape2: ', prediction2.shape)
        
        prediction3 = prediction.reshape(512, 512)
        print('Prediction shape3: ', prediction3.shape)        
		
		# Save the results as .tif file.
		# Copy the coorindate system information, image size and other metadata from the satellite image 
        outputMeta = image_dataset.meta
		# Change the number of bands and data type.
        outputMeta.update(count=1, dtype='float32')
        # Writing the image on the disk
        with rasterio.open(predictedImageFile, 'w', **outputMeta) as dst:
            dst.write(prediction3, 1)
        
        print('Predicting took: ', round((time.time() - start_time), 1), ' seconds')
        
        
model = load_model(model_final) #load_model ??
        
# Read all the training files
all_frames = os.listdir(prediction_data_dir)
for img in all_frames:
    predictImage(model, img)
#Step 9
#Test on the image form test folders

#x = img_to_array(img)
#x = np.expand_dims(x, axis=0)
#preds = test_model.predict_classes(x)
#prob = test_model.predict_proba(x)
#print(preds, prob)
    
    #src = rasterio.open('C:\\temp\\ML_course_data\\tiles\\labels650\\forest_spruce_scaled_1_1.tif').read()