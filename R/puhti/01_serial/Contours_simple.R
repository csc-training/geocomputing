# This is an spatial analysis example script for using R in CSC Puhti
# This scipt can be used for serial or array jobs.
# Here countours are calculated based on a DEM file and saved in GeoPackage format.
# The file given as input is a 10m DEM file from Finnish NLS.

# load raster and sp libraries
library(raster)
library(rgdal)

# Set the working directory with RStudio
# mainDir <- "/scratch/project_2002044/students/ekkylli/geocomputing/R/puhti/01_serial"
# setwd(mainDir)

mapsheets <- readLines('../mapsheets.txt')

#Calculate contours and save the results as GeoPackage
for (mapsheet in mapsheets){
  DEM <- raster(mapsheet)
  file <- gsub("tif", "gpkg", basename(mapsheet))
  contours<-rasterToContour(DEM)
  writeOGR(contours, dsn = file, layer = "contours", driver = "GPKG", overwrite_layer=TRUE)
}