# This is an spatial analysis example script for using R in CSC Puhti
# This scipt can be used for serial or array jobs.
# Here countours are calculated based on a DEM file and saved in Shape format.
# The file given as input is a 10m DEM file from Finnish NLS.

# load raster library
library(raster)

#Set the names of the folders.
mainDir <- "/scratch/project_2002044/students/training011/R_spatial_exercises/01_serial"
shapeFolder <- "shape"

# Set the working directory
setwd(mainDir)

mapsheets <- readLines('../mapsheets.txt')

#Make folders for files, do not make, if already exist
if (!dir.exists(shapeFolder)) {
  dir.create(shapeFolder)
}

#Calculate contours and save a shape file
for (mapsheet in mapsheets){
  DEM <- raster(mapsheet)
  shapefile <- file.path(shapeFolder, gsub("tif", "shp", basename(mapsheet)))
  contours<-rasterToContour(DEM)
  shapefile(contours, filename=shapefile, overwrite=TRUE)
  plot(DEM)
  plot(contours, add=TRUE)
}