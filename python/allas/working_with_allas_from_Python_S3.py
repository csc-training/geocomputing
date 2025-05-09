#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 13:57:52 2019
@author: ekkylli
Updated 7.7.2025
"""

# Example script for using Allas directly from an Python script:
# - Reading raster and vector files
# - Writing raster and vector files
# - Looping over all files of certain type in a bucket

# Please notice that this example works ONLY with GDAL-based libraries for spatial data: rasterio, geopandas etc.

# The required packages depend on the task
# For working with rasters
import rasterio
# For working with vectors
import geopandas as gpd
# For listing files and writing to Allas
import boto3
import os


# Before starting to use S3, set up your credentials and endpoint. 
# This example here applies for using Allas from CSC Puhti or Mahti supercomputers.
# To use some other S3 stroage or from some other computer,
# See https://docs.csc.fi/support/tutorials/gis/gdal_cloud/#s3-connection-details
#
# 1) Set up your credentials to Allas:
# module load allas
# allas-conf --mode s3cmd
# This is needed only once, as long as you are using the same CSC project.
# This also sets S3 endopoint to .aws/config file in a way understandable for boto3 library, but not for GDAL.
#
# 2) Set S3-endpoint for GDAL-library:
# module load allas
# OR
os.environ["AWS_S3_ENDPOINT"] = "a3s.fi"
# This sets AWS_S3_ENDPOINT environment variable to "a3s.fi".
# Environment variables are cleaned after session end, so it must be set again in each new session.

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
# Then print the extent of each file as example.

# Create connection to S3 storage
os.environ["AWS_REQUEST_CHECKSUM_CALCULATION"] = "when_required"
os.environ["AWS_RESPONSE_CHECKSUM_VALIDATION"] = "when_required"
s3_resource = boto3.resource('s3')

# By default boto3 is connecting to Amazon S3, to use custom endpoint, define it in .aws/config file as done by allas-conf --mode s3cmd
# OR define it in the Python code
# s3_resource = boto3.resource("s3", endpoint_url='https://a3s.fi')

my_bucket = s3_resource.Bucket('name_of_your_Allas_bucket')

for my_bucket_object in my_bucket.objects.all():
    if (my_bucket_object.key.endswith('.tif')):    
        filePath = '/vsis3/gis-int2/' + my_bucket_object.key
        print(filePath)
        r = rasterio.open(filePath)
        print(r.bounds)
        


