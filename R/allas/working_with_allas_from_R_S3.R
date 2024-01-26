# Example script for using Allas directly from an R script:
# - Reading and wrtiing raster and vector files
# - Looping over all files of certain type in a bucket
# - Writing raster and vector files (not working properly) Older version

# Please notice that this example works ONLY with GDAL-based libraries for spatial data: sf, terra etc.

library("terra")
library("sf")
library("aws.s3")
library("tidyverse")

# Before starting to use Allas with aws.s3 set up your connection to Allas.
# In Puhti run:
#
# module load allas
# OR
# Add to your ~/.Renviron-file a new row
# AWS_S3_ENDPOINT=a3s.fi
# OR
# Sys.setenv("AWS_S3_ENDPOINT" = "a3s.fi")
# This sets AWS_S3_ENDPOINT environment variable to "a3s.fi".
# Environment variables are cleaned after session end, so it must be set again in each new session.
# OR
# If using some MPI-library some other way may be needed for setting the environment variable, 
# for example in snow this should be used, so that also workers get it:
# clusterEvalQ(cl, Sys.setenv("AWS_S3_ENDPOINT" = "a3s.fi"))
#
# allas-conf --mode s3cmd
# This creates [.aws/credentials](https://github.com/cloudyr/aws.signature/) to your home directory
# The credentials are saved to a file, so they need to be set only once from a new computer or when changing project.

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
all_files_in_bucket <- get_bucket_df(name_of_your_Allas_bucket, region='')
# Filter out only .tif-files and keep only the file name information (=Key)
tif_files = all_files_in_bucket %>% filter(str_detect(Key, '.tif$')) %>% select(Key)
# Loop through the files, here just printing the extent of each file as example.
for (row in 1:nrow(tif_files)) {    
  filepath <- paste('/vsis3/name_of_your_Allas_bucket/', tif_files[row,], sep = "")
  print (filepath)
  r <- raster(filepath)
  print (extent(r))
}

# *****        
# Older option to write files that likely is not needed any more.
# Note, for some reason R can not read these files back again, during the same R session.

# Writing raster file
s3write_using(r, FUN = raster::writeRaster,
              bucket = "name_of_your_Allas_bucket",
              object = "name_of_your_output_raster_file.tif",
              opts=c(region=""))


# Writing vector file
s3write_using(v, FUN = sf::st_write, layer='name_of_your_output_layer',
              bucket = "name_of_your_Allas_bucket",
              object = "name_of_your_output_vector_file.gpkg",
              opts=c(region=""))



