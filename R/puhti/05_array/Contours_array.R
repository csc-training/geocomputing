# This is an spatial analysis example script for using R in CSC Puhti
# This script can be used for serial or array jobs.
# Here a .tif DEM file is provided as an argument
# and then countours are calculated and saved in GeoPackage format.
# The file given as input is a 10m DEM file from Finnish NLS.

# Load the necessary libraries
library(terra)

# Read the command line argument, which is the path of the .tif file.
args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("Please give the map sheet number", call.=FALSE)
} else if (length(args)==1) {
  # The filepath given to this script goes to variable mapsheet
  mapsheet <- args[1]
}
print(mapsheet)

# Calculate contours 
DEM <- rast(mapsheet)
file <- gsub("tif", "gpkg", basename(mapsheet))
contours <- as.contour(DEM)
# Save the results as GeoPackage
writeVector(contours, file, filetype="GPKG", overwrite=TRUE)
