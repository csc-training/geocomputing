# This is an spatial analysis example script for using R in CSC Puhti
# This script can be used for serial or array jobs.
# Here a .tif DEM file is provided as an argument
# and then countours are calculated and saved in Shape format.
# The file given as input is a 10m DEM file from Finnish NLS.

# Load the necessary libraries
library(raster)

# Read the command line argument, which is the path of the .tif file.
args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("Please give the map sheet number", call.=FALSE)
} else if (length(args)==1) {
  # The filepath given to this script goes to variable mapsheet
  mapsheet <- args[1]
}
print(mapsheet)

# Set the working directory to the current directory
setwd(getSrcDirectory()[1])

# Create output folder if it does not exist
shapeFolder <- "shape"
if (!dir.exists(shapeFolder)) {
  dir.create(shapeFolder)
}

# Calculate contours with 50m intervals, from 200 to 750m
DEM <- raster(mapsheet)
shapefile <- file.path(shapeFolder, gsub("tif", "shp", basename(mapsheet)))
contours<-rasterToContour(DEM)
shapefile(contours, filename=shapefile, overwrite=TRUE)

# If working locally, you can plot both files
plot(DEM)
plot(contours, add=TRUE)
