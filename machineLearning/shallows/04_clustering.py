# In this exercise k-means clustering is used for finding 5 clusters from a 4 band Sentinel satellite image.

import spectral
import rasterio
import numpy as np
import os

### FILL HERE the path where your data is. e.g "/scratch/project_2000599/students/26/data"
wrkFolder = ""
inputImage =  os.path.join(wrkFolder,'T34VFM_20180829T100019_clipped_scaled.tif')

def run_model(image_data):
    # scaling back reflectance values to be between 0 and 1
    scaled_input_data = image_data / 10000

    # Check shape of input data
    scaled_input_data.shape

    # Spectral.kmeans function expects data in width x height x bands format.
    # So we have to change the axis order, moving the bands axis to last.
    input_data2 = np.transpose(scaled_input_data, (1, 2, 0))
    # Check that now data is in correct format.
    input_data2.shape
    # Calculate clusters, interested in 5 classes and 5 iterations.
    classes, centers = spectral.kmeans(input_data2, nclusters=5, max_iterations=5)
    return classes, centers


def predict_image(classes, meta):
    # Save the result to a GeoTiff file
    # First prepare the metadata of new file,
    # compared to original file, we will have only 1 band, different format and data type.
    meta.update(count=1, driver='GTiff', dtype='int8')
    # Check the data type of classes array
    classes.dtype
    # Rasterio does not support int64.
    # See https://github.com/mapbox/rasterio/blob/master/rasterio/dtypes.py for available data types in Rasterio.
    # So change the data type to int8, as we have only integers 0 to 4 in our result dataset, int8 is enough.
    classes_int8 = classes.astype('int8')

    # Check that data type is now correct
    classes_int8.dtype

    # Save the results to predict.tif
    with rasterio.open('predicted.tif', 'w', **meta) as dst:
        dst.write(classes_int8, 1)


def main():
    # Read the input dataset with Rasterio
    input_dataset = rasterio.open(inputImage)
    input_data = input_dataset.read()
    classes, centers = run_model(input_data)
    predict_image(classes, input_dataset.meta)


if __name__ == '__main__':
    main()
