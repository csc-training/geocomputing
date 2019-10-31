# In this exercise k-means clustering is used for finding 7 clusters from a 3 band Sentinel satellite image.

from sklearn.cluster import KMeans
import rasterio
import numpy as np
import os
import time

### FILL HERE the path where your data is. e.g "/scratch/project_2000599/students/26/data"
base_folder = "/tmp/gis-ml/data/forest"
inputImage =  os.path.join(base_folder,'T34VFM_20180829T100019_clipped_scaled.tif')
outputImage = os.path.join(base_folder,'T34VFM_20180829T100019_KMeans.tif')

# Read data and shape it to suitable form for scikit-learn
def prepareData(image_dataset):    
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
    
    return pixels    

def runModel(image_data):
    # Calculate clusters, interested in 5 classes and 5 iterations.
    classes = KMeans(n_clusters=7, random_state=63, max_iter=10, n_jobs=4).fit_predict(image_data)
    return classes


def saveClassifiedImage(classes, meta):   
    print ('Dataframe shape, output, 1D: ', classes.shape) 
    
    #Reshape back to 2D    
    classes2D = np.reshape(classes, (meta['height'], meta['width']))
    print ('Dataframe shape, output after reshape, 2D: ', classes2D.shape)     
    
    # Save the result to a GeoTiff file
    # First prepare the metadata of new file,
    # compared to original file, we will have only 1 band and int32 data type.
    meta.update(count=1, dtype='int32')
    # Save the data
    with rasterio.open(outputImage, 'w', **meta) as dst:
        dst.write(classes2D, 1)


def main():
    # Read the input dataset with Rasterio
    input_dataset = rasterio.open(inputImage)
    input_data = prepareData(input_dataset)
    classes = runModel(input_data)
    saveClassifiedImage(classes, input_dataset.meta)


if __name__ == '__main__':
    ### This part just runs the main method and times it
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(round((end - start),0)) + " seconds")

