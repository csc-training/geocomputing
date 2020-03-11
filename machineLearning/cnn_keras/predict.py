# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 12:46:58 2020

@author: ekkylli
"""
import os, time, glob
from osgeo import gdal 
import numpy as np
import rasterio
import rasterio.merge
from tensorflow.keras.models import load_model

#SETTINGS


# Paths for INPUTS: data and model
#data_dir='/scratch/project_2002044/test/johannes/tiles'
data_dir='C:\\temp\\ML_course_data\\tiles_new'
model_name='mc_5000_4_2'
results_dir=data_dir
#results_dir='/scratch/project_2002044/test/kylli'
prediction_data_dir = os.path.join(data_dir, 'image_prediction_tiles_512')
test_tiles_file = os.path.join(data_dir, 'test_tiles.csv')
model_final = os.path.join(results_dir, 'model_best_'+model_name+'.h5')

#Paths for RESULTS
predicted_tiles = os.path.join(results_dir,'precitions512_'+model_name)
prediction_image_file = os.path.join(results_dir,'predicted_spruce_'+model_name+'.tif')
prediction_vrt = os.path.join(results_dir,'predicted_spruce_'+model_name+'.vrt')


img_size = 512
img_channels = 3
no_of_classes=4 #Change for multi-class 4

# Predict a tile and save it as .tif file
def predictTile(model, dataImage):
    # Set the file paths
    
    #dataForPredictionFile = os.path.join(prediction_data_dir, dataImage)	
    predictedImageFile = os.path.join(predicted_tiles, os.path.basename(dataImage))
    
    
    with rasterio.open(dataImage, 'r') as image_dataset:    
        print(dataForPredictionFile)
        # Read the data image
        image_data = image_dataset.read()
        #Reorder axis for Keras, channel last
        image_data2 = np.transpose(image_data, (1, 2, 0)) 
        print(image_data2.shape)
        #Reshape data for Keras, add extra dimension,  
        image_data3 = image_data2.reshape(1, img_size, img_size, img_channels)
        
        # predicting the probability of each pixel
        prediction = model.predict(image_data3)
        #print(prediction.shape)
        # Find the class with best probability
        if no_of_classes > 1: 
            prediction = np.argmax(prediction, 3)
        
		# Reshape for rasterio       
        prediction2 = prediction.reshape(img_size, img_size)     
		
		# Save the results as .tif file.
		# Copy the coorindate system information, image size and other metadata from the satellite image 
        outputMeta = image_dataset.meta
		# Change the number of bands and data type.
        if no_of_classes == 1: 
            dtype='float32'  
        else:
            prediction2 = prediction2.astype(np.int16)
            dtype='int16'
        outputMeta.update(count=1, dtype=dtype)
        # Writing the image on the disk
        with rasterio.open(predictedImageFile, 'w', **outputMeta) as dst:
            print(predictedImageFile)
            dst.write(prediction2, 1)

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]
               
def  mergeTiles():
    tile_files = listdir_fullpath(predicted_tiles)

    my_vrt = gdal.BuildVRT(prediction_vrt, tile_files)
    my_vrt = None    
       
    with rasterio.open(prediction_vrt, 'r') as vrt_in:
        out_metafile = vrt_in.meta.copy()
        out_metafile.update({"driver": "GTiff"})
        with rasterio.open(prediction_image_file, "w", **out_metafile) as dest:
            dest.write(vrt_in.read())  

def main():
    # Load the previously trained model
    model = load_model(model_final) 
            
    # Predict for all tiles
    all_frames = glob.glob(prediction_data_dir+"/*.tif")
    # Make a folder for the predicted tiles
    os.makedirs(predicted_tiles, exist_ok=True)
    for tile in all_frames:
        predictTile(model, tile)
        
    mergeTiles()
       
if __name__ == '__main__':
    ### This part just runs the main method and times it
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(round((end - start),0)) + " seconds")    
#Step 9
#Test on the image form test folders

#x = img_to_array(img)
#x = np.expand_dims(x, axis=0)
#preds = test_model.predict_classes(x)
#prob = test_model.predict_proba(x)
#print(preds, prob)
    
    #src = rasterio.open('C:\\temp\\ML_course_data\\tiles\\labels650\\forest_spruce_scaled_1_1.tif').read()