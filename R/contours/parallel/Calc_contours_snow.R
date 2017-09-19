# This is an spatial analysis example script for using R in CSC Taito
# This scipt can be used for parallel jobs.
# Here 3 .tif files are saved to SagaGIS format
# and then countours are calculated and saved in Shape format.
# The file given as input is a 10m DEM file from Finnish NLS.
# The input files are listed in the mapsheet.txt file

# For parallel tasks the snow package is used.

#Set the names of the folders.
mainDir <- "~/R_spatial_2017_4"
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

# Read the mapsheets from external file
mapsheets <- readLines('~/R-with-Taito/R-with-Taito/examples/snow/mapsheets.txt')

# Start the snow cluster
cl<-getMPIcluster()

# The function run on each core
# The R modules need to be loaded inside the functions.
# The variables from outside of this function are not visible.
funtorun<-function(mapsheet) {

  # SagaGIS needs the input in its own format, so let's change the original .tif file to Saga format.
  gridfile <- file.path(gridFolder, gsub("tif", "sdat", basename(mapsheet)))
  gdal_translate(mapsheet, gridfile, of="SAGA",verbose=TRUE)


  # Calculate contours with 50m intervals, from 200 to 750m
  shapefile <- file.path(shapeFolder, gsub("tif", "shp", basename(mapsheet)))
  gridfile <- gsub("sdat", "sgrd", gridfile)
  rsaga.contour(gridfile, shapefile, 50, 200, 750, env = rsaga.env())

  #The tool gives like other RSAGA tools "Error: select a tool" message, but it actually is working :)
}

# load RSAGA and rgdal libraries
clusterEvalQ(cl, library(RSAGA))
clusterEvalQ(cl, library(gdalUtils))

#Export variable to each cluster
clusterExport(cl, "mainDir")
clusterExport(cl, "gridFolder")
clusterExport(cl, "shapeFolder")

#Set working directory
clusterEvalQ(cl, setwd(mainDir))

# Read the mapsheets from external file
mapsheets <- readLines('~/git/geocomputing/R/contours/mapsheets.txt')

# Give cluster the work to be done
system.time(a<-clusterApply(cl,mapsheets,funtorun))

#Stop cluster
stopCluster(cl)

#quit()
