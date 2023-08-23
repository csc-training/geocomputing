#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 13:57:52 2019
@author: ekkylli
"""

# Example script for using Allas directly from an Python script:
# - Reading raster and vector files
# - Writing raster and vector files
# - Looping over all files of certain type in a bucket
# - Older option to write files that likely is not needed any more.

# The required packages depend on the task
# For working with rasters
import rasterio
# For working with vectors
import geopandas as gpd
# For listing files and writing to Allas
import boto3
import os


# Before starting to use Allas with S3 set up your connection to Allas.
# In Puhti run:
#
# module load allas
# OR
# os.environ["AWS_S3_ENDPOINT"] = "a3s.fi"
# This sets AWS_S3_ENDPOINT environment variable to "a3s.fi".
# Environment variables are cleaned after session end, so it must be set again in each new session.
#
# allas-conf --mode s3cmd
# This creates [.aws/credentials-file](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) to your home directory
# The credentials are saved to a file, so they need to be set only once from a new computer.

# If you want to WRITE files with rasterio/geopandas directly to Allas, set also this.
os.environ["CPL_VSIL_USE_TEMP_FILE_FOR_RANDOM_WRITE"] = "YES"

# Reading raster file
r = rasterio.open('/vsis3/name_of_your_Allas_bucket/name_of_your_input_raster_file.tif')
input_data = r.read()

# Writing raster file
with rasterio.open('/vsis3/name_of_your_Allas_bucket/name_of_your_output_raster_file.tif', 'w', **r.profile) as dst:
    dst.write(input_data)

# Reading vector file
v = gpd.read_file('/vsis3/name_of_your_Allas_bucket/name_of_your_input_vector_file.gpkg')

# Writing vector file
v.to_file('/vsis3/name_of_your_Allas_bucket/name_of_your_output_vector_file.gpkg', layer='layername', driver="GPKG")

# Looping through all files in a bucket, find ones that are tifs.
# Then just print the extent of each file as example.

# Set the end-point correctly for boto3
s3 = boto3.client("s3", endpoint_url='https://a3s.fi')

for key in s3.list_objects_v2(Bucket='name_of_your_Allas_bucket')['Contents']:
    if (key['Key'].endswith('.tif')):
        filePath = '/vsis3/name_of_your_Allas_bucket/' + key['Key']
        print(filePath)
        r = rasterio.open(filePath)
        print(r.bounds)
        
# *****        
# Older option to write files that likely is not needed any more.
# Writing raster file using boto3 library


# For writing rasters to Allas (older option)
from rasterio.io import MemoryFile
# For writing vectors to Allas (older option)
import tempfile

# Create the raster file to memory and write to Allas
with MemoryFile() as mem_file:
    with mem_file.open(**r.profile) as dataset:
        print(dataset.meta)
        dataset.write(input_data)
        #Write to Allas
    s3.upload_fileobj(mem_file, 'name_of_your_Allas_bucket', 'name_of_your_output_raster_file.tif')

# Create the vector file to memory and write to Allas
tmp = tempfile.NamedTemporaryFile()
v.to_file(tmp, layer='test', driver="GPKG")
#Move the tmp pointer to the beginning of temp file.
tmp.seek(0)
#Write to Allas
s3.upload_fileobj(tmp, 'name_of_your_Allas_bucket', 'name_of_your_output_vector_file.gpkg')


