# This is an spatial analysis example script for using R in CSC Puhti
# This script can be used for parallel jobs.
# The countours are calculated and saved in GeoPackage format.
# The file given as input is a 10m DEM file from Finnish NLS.
# The input files are listed in the mapsheet.txt file

# For parallel tasks future package is used.

# load libraries
library(furrr)
library(raster)
library(rgdal)

options(future.availableCores.methods = "Slurm")

# With plan(multicore) the number of workers is based on batch job reservation details.
plan("multicore")

# The function run on each core
funtorun <- function(mapsheet) {
  DEM <- raster(mapsheet)
  file <- gsub("tif", "gpkg", basename(mapsheet))
  contours<-rasterToContour(DEM)
  writeOGR(contours, dsn = file, layer = "contours", driver = "GPKG", overwrite_layer=TRUE)
}

# Read the mapsheets from external file
mapsheets <- readLines('../mapsheets.txt')

# Give cluster the work to be done
system.time(a<-future_map(mapsheets,funtorun))
