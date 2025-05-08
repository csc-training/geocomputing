# Example script for using Allas directly from an R script:
# - Reading and wrtiing raster and vector files
# - Looping over all files of certain type in a bucket
# - Writing raster and vector files (not working properly) Older version

# Please notice that this example works ONLY with GDAL-based libraries for spatial data: sf, terra etc.

# Note this does not work with R version 442 in Puhti, use some other version.

library("terra")
library("sf")
library("aws.s3")
library("tidyverse")

# Before starting to use Allas with aws.s3 set up your credentials and endpoint to Allas.
# This example here applies for using Allas from CSC Puhti or Mahti supercomputers.
# To use some other S3 stroage or from some other computer,
# See https://docs.csc.fi/support/tutorials/gis/gdal_cloud/#s3-connection-details

# 1) Set up your credentials to Allas:
# module load allas
# allas-conf --mode s3cmd
# This is needed only once, as long as you are using the same CSC project.
# This also sets S3 endopoint to .aws/config file.

# 2) Set S3 region for aws.s3-library.
options("cloudyr.aws.default_region" = "")

# If you want to WRITE files with terra/sf directly to Allas, set also this.
Sys.setenv("CPL_VSIL_USE_TEMP_FILE_FOR_RANDOM_WRITE" = "YES")

# Reading raster file
r <- rast('/vsis3/name_of_your_Allas_bucket/name_of_your_input_raster_file.tif')

# This should work, but has had some bugs in terra code, so does not work with any R version in Puhti (8.8.2023)
writeRaster(r, filename='/vsis3/name_of_your_Allas_bucket/name_of_your_output_raster_file.tif')

# Reading vector file
v <- st_read('/vsis3/name_of_your_Allas_bucket/name_of_your_input_vector_file.gpkg')

# Writing vector file
st_write(v, '/vsis3/name_of_your_Allas_bucket/name_of_your_output_vector_file.gpkg')

# Looping through all files in a bucket, having the same file type (tif).
# First get list of all objects in the bucket
all_files_in_bucket <- get_bucket_df(name_of_your_Allas_bucket)
# Filter out only .tif-files and keep only the file name information (=Key)
tif_files = all_files_in_bucket %>% filter(str_detect(Key, '.tif$')) %>% select(Key)
# Loop through the files, here just printing the extent of each file as example.
for (row in 1:nrow(tif_files)) {    
  filepath <- paste('/vsis3/name_of_your_Allas_bucket/', tif_files[row,], sep = "")
  print (filepath)
  r <- raster(filepath)
  print (extent(r))
}


