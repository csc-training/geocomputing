# This is an spatial analysis example script for using R in CSC Puhti
# This script can be used for parallel jobs.
# Here 3 .tif files are saved to SagaGIS format
# and then countours are calculated and saved in Shape format.
# The file given as input is a 10m DEM file from Finnish NLS.
# The input files are listed in the mapsheet.txt file

# For parallel tasks future package is used.

# load libraries
library(furrr)
library(raster)

#Set the names of the folders.
mainDir <- "/scratch/project_xx/R/04_future"
shapeFolder <- "shape"

# Set the working directory
setwd(mainDir)

#Make folders for files, do not make, if already exist
if (!dir.exists(shapeFolder)) {
  dir.create(shapeFolder)
}

# Start the snow cluster and create a plan with future package
cl<-getMPIcluster()
plan(cluster, workers = cl)

# The function run on each core
funtorun <- function(mapsheet) {
  DEM <- raster(mapsheet)
  shapefile <- file.path(shapeFolder, gsub("tif", "shp", basename(mapsheet)))
  contours<-rasterToContour(DEM)
  shapefile(contours, filename=shapefile, overwrite=TRUE)
}

# Read the mapsheets from external file
mapsheets <- readLines('../mapsheets.txt')

# Give cluster the work to be done
system.time(a<-future_map(mapsheets,funtorun))

#Stop cluster
stopCluster(cl)

