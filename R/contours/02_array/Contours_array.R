# This is an spatial analysis example script for using R in CSC Puhti
# This scipt can be used for serial or array jobs.
# Here a .tif file provided as argument is save to SagaGIS format
# and then countours are calculated and saved in Shape format.
# The file given as input is a 10m DEM file from Finnish NLS.

#Read the command line argument, which is the path of the .tif file.
args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("Please give the map sheet number", call.=FALSE)
} else if (length(args)==1) {
  # default output file
  mapsheet <- args[1]
}
print(mapsheet)
# load RSAGA and gdalUtils libraries
library(raster)

#Set the names of the folders.
mainDir <- "/scratch/project_2002044/students/training011/R_spatial_exercises/02_array"
shapeFolder <- "shape"

# Set the working directory
setwd(mainDir)

#Make folders for files, do not make, if already exist
if (!dir.exists(shapeFolder)) {
  dir.create(shapeFolder)
}

# Calculate contours with 50m intervals, from 200 to 750m
DEM <- raster(mapsheet)
shapefile <- file.path(shapeFolder, gsub("tif", "shp", basename(mapsheet)))
contours<-rasterToContour(DEM)
shapefile(contours, filename=shapefile, overwrite=TRUE)
plot(DEM)
plot(contours, add=TRUE)
