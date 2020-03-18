# -*- coding: utf-8 -*-
"""
Script for predicting/interference based on a CNN segmentation model based on GeoTiff tiles.
As last the tiles are merged to one big image.
The model may be binary or multi-class, set no_of_classes accordingly.
The main Python libraries are Keras, rasterio and numpy.

Created on Fri Mar  6 12:46:58 2020

@author: ekkylli
"""
import os, time, glob
from osgeo import gdal 
import numpy as np
import rasterio
import rasterio.merge
from tensorflow.keras.models import load_model
from loss_jaccard import jaccard_loss

#SETTINGS

# Paths for INPUTS: data and model
data_dir='/scratch/project_2002044/test/johannes/tiles'
results_dir='/scratch/project_2002044/test/kylli'
#TODO clean away
#data_dir='C:\\temp\\ML_course_data\\tiles_new'
#results_dir=data_dir

model_name='spruce_5000_3_2_weighted1_10'
prediction_data_dir = os.path.join(data_dir, 'image_prediction_tiles_512')
model_final = os.path.join(results_dir, 'model_best_'+model_name+'.h5')

#Paths for RESULTS
predicted_tiles_folder = os.path.join(results_dir,'precitions512_'+model_name)
prediction_image_file = os.path.join(results_dir,'predicted_spruce_'+model_name+'.tif')
prediction_vrt_file = os.path.join(results_dir,'predicted_spruce_'+model_name+'.vrt')

#Setting of the data
img_size = 512
img_channels = 3
# The number of classes in labels
# TOFIX: Change the number according to the used data
no_of_classes=2 #For binary classification
# no_of_classes=4 # n for multiclass

# Predict a tile and save it as .tif file
def predictTile(model, dataImage):
    # Set the file paths    
    predictedImageFile = os.path.join(predicted_tiles_folder, os.path.basename(dataImage))
    
    
    with rasterio.open(dataImage, 'r') as image_dataset:    
        # Read the data image
        image_data = image_dataset.read()
        
        #Reorder axis for Keras, channel last
        image_data2 = np.transpose(image_data, (1, 2, 0)) 
        
        #Reshape data for Keras, add extra dimension,  
        image_data3 = image_data2.reshape(1, img_size, img_size, img_channels)
        
        # predicting the probability of each pixel
        prediction = model.predict(image_data3)

        # If multi-class, find the class with best probability
        if no_of_classes > 2: 
            prediction = np.argmax(prediction, 3)
        
		# Reshape for rasterio       
        prediction2 = prediction.reshape(img_size, img_size)     
		
		# Save the results as .tif file.
		# Copy the coorindate system information, image size and other metadata from the satellite image 
        outputMeta = image_dataset.meta
		# Change the data type in file meta.
        if no_of_classes == 2: 
            dtype='float32'  
        else:
            #For multi-class change also data type, argmax output is in int64 not supported by rasterio.
            prediction2 = prediction2.astype(np.uint8)
            dtype='ubyte'
        outputMeta.update(count=1, dtype=dtype)
        # Writing the image on the disk
        with rasterio.open(predictedImageFile, 'w', **outputMeta) as dst:
            dst.write(prediction2, 1)


               
# Merge all tiles to one big .tif-image
def  mergeTiles():
    
    #Find all .tif files in the predicted tiles folder
    tile_files = glob.glob(predicted_tiles_folder+"/*.tif")
    
    # Make first GDAL virtual raster of the tiles.
    my_vrt = gdal.BuildVRT(prediction_vrt_file, tile_files)
    # set my_vrt to None, because only then GDAL writes the file to disk.
    my_vrt = None    
       
    # Save the virtual raster to one file.
    # If really a lot of tiles, add some logic to output several files.
    with rasterio.open(prediction_vrt_file, 'r') as vrt_in:
        out_metafile = vrt_in.meta.copy()
        out_metafile.update({"driver": "GTiff"})
        with rasterio.open(prediction_image_file, "w", **out_metafile) as dest:
            dest.write(vrt_in.read())  

def main():
    # Load the previously trained model
    model = load_model(model_final, custom_objects={'jaccard_loss': jaccard_loss}) 
    
    # Find all data tiles for prediction
    all_frames = glob.glob(prediction_data_dir+"/*.tif")
    # Make a folder for the predicted tiles
    os.makedirs(predicted_tiles_folder, exist_ok=True)
    
    # Predict for all tiles
    for tile in all_frames:
        predictTile(model, tile)
    
    #Merge tiles to one GeoTiff    
    mergeTiles()
       
if __name__ == '__main__':
    ### This part just runs the main method and times it
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(round((end - start),0)) + " seconds")    