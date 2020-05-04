# Example script for using Allas directly from an R script:
# - Reading raster and vector files
# - Looping over all files of certain type in a bucket
# - Writing raster and vector files (not working properly)

library("raster")
library("sf")
library("aws.s3")
library("tidyverse")

# Before starting to use Allas with aws.s3 set up your connection to Allas.
# In Puhti run:
#
# module load allas
# OR
# Sys.setenv("AWS_S3_ENDPOINT" = "a3s.fi")
# This sets AWS_S3_ENDPOINT environment variable to "a3s.fi".
# Environment variables are cleaned after session end, so it must be set again in each new session.
#
# allas-conf --mode s3cmd
# This creates [.s3cfg](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) to your home directory
# The credentials are saved to a file, so they need to be set only once from a new computer.

# Reading raster file
r <- raster('/vsis3/name_of_your_Allas_bucket/name_of_your_input_raster_file.tif')

# Reading vector file
v <- st_read('/vsis3/name_of_your_Allas_bucket/name_of_your_input_vector_file.gpkg')

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

# Writing files.
# Note, for some reason R can not read these files back again, during the same R session.

# Writing raster file
s3write_using(r, FUN = raster::writeRaster,
              bucket = "name_of_your_Allas_bucket",
              object = "name_of_your_output_raster_file.tif",
             region='')


# Writing vector file
s3write_using(v, FUN = sf::st_write, layer='name_of_your_output_layer',
              bucket = "name_of_your_Allas_bucket",
              object = "name_of_your_output_vector_file.gpkg",
             region='')



