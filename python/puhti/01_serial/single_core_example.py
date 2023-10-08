"""
An example Python script how to calculate NDVI for one Sentinel satellite image
using just 1 process.

Author: Johannes Nyman, Kylli Ek, Samantha Wittke CSC

"""
import os
import sys
import time
import rasterio


### The filepath for the input Sentinel image that is given as input parameter
sentinel_image_path = sys.argv[1]

def readImage(image_folder_fp):
    print(f"Reading Sentinel image from: {image_folder_fp}")
    ### Rather than figuring out what the filepath inside SAFE folder is, this is just finding the red and nir files with correct endings
    for subdir, dirs, files in os.walk(image_folder_fp):
        for file in files:
            if file.endswith("_B04_10m.jp2"):
                red_fp = os.path.join(subdir,file)
            if file.endswith("_B08_10m.jp2"):
                nir_fp = os.path.join(subdir,file)
    ### Read the red and nir (near-infrared) band files with Rasterio
    red = rasterio.open(red_fp)
    nir = rasterio.open(nir_fp)
    ### Return the rasterio objects as a list
    return red,nir

def calculateNDVI(red,nir):
    print("Computing NDVI")
    ### This function calculates NDVI from the red and nir bands
    ## Read the rasterio objects pixel information to numpy arrays
    red = red.read(1)
    nir = nir.read(1)
    ### Scale the image values back to real reflectance values (sentinel pixel values have been multiplied by 10000)
    red = red /10000
    nir = nir /10000
    ### the NDVI formula
    ndvi = (nir - red) / (nir + red)
    return ndvi

def saveImage(ndvi, sentinel_image_path, input_image):
    ## Create an output folder to this location, if it does not exist
    outputdir = 'output'
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    ## Create output filepath for the image. We use the input name with _NDVI end
    output_file = os.path.join(outputdir, os.path.basename(sentinel_image_path).replace(".SAFE", "_NDVI.tif"))
    print(f"Saving image: {output_file}")
    ## Copy the metadata (extent, coordinate system etc.) from one of the input bands (red)
    metadata = input_image.profile
    ## Change the data type from integer to float and file type from jp2 to GeoTiff
    metadata.update(
        dtype=rasterio.float64,
        driver='GTiff')
    ## Write the ndvi numpy array to a GeoTiff with the updated metadata
    with rasterio.open(output_file, 'w', **metadata) as dst:
        dst.write(ndvi, 1)

def processImage(sentinel_image_path):
    ### This function processes one image (read, compute, save)
    ## Read the image and get rasterio objects from the red nir bands
    red, nir = readImage(sentinel_image_path)
    ## Calculate NDVI and get the resulting numpy array
    ndvi = calculateNDVI(red,nir)
    ## Write the NDVI numpy array to file to the same extent as the red input band
    saveImage(ndvi,sentinel_image_path,red)

def main():

    print(f"\nProcess of {sentinel_image_path} started")
    processImage(sentinel_image_path)
    print(f"Processing of {sentinel_image_path} done\n")

if __name__ == '__main__':
    ## This part is the first to execute when script is ran. It times the execution time and rans the main function
    start = time.time()
    main()
    end = time.time()
    print(f"Script completed in {str(end - start)} seconds")
