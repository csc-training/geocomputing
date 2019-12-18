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

# load RSAGA and gdalUtils libraries
library(RSAGA)
library(gdalUtils)

#Set the names of the folders.
mainDir <- "~/R_spatial_2017_3"
gridFolder <- "1_grid"
shapeFolder <- "2_shape"

# Set the working directory
if (!dir.exists(mainDir)) {
  dir.create(mainDir)
}
setwd(mainDir)

#Make folders for files, do not make, if already exist
if (!dir.exists(shapeFolder)) {
  dir.create(shapeFolder)
}

if (!dir.exists(gridFolder)) {
  dir.create(gridFolder)
}

# SagaGIS needs the input in its own format, so let's change the original .tif file to Saga format.
gridfile <- file.path(gridFolder, gsub("tif", "sdat", basename(mapsheet)))
gdal_translate(mapsheet, gridfile, of="SAGA")


# Calculate contours with 50m intervals, from 200 to 750m
shapefile <- file.path(shapeFolder, gsub("tif", "shp", basename(mapsheet)))
gridfile <- gsub("sdat", "sgrd", gridfile)
rsaga.contour(gridfile, shapefile, 50, 200, 750, env = rsaga.env())

#The tool gives like other RSAGA tools "Error: select a tool" message, but it actually is working :)

quit()
