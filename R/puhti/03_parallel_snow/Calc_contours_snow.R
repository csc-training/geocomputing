# This is an spatial analysis example script for using R in CSC Puhti
# This scipt can be used for parallel jobs.
# Here countours are calculated and saved in GeoPackage format.
# The file given as input is a 10m DEM file from Finnish NLS.
# The input files are listed in the mapsheet.txt file

# For parallel tasks the snow package is used.

# Start the snow cluster
cl<-getMPIcluster()

# The function run on each core
# The R modules need to be loaded inside the functions.
# The variables from outside of this function are not visible.
funtorun<-function(mapsheet) {
  DEM <- rast(mapsheet)
  file <- gsub("tif", "gpkg", basename(mapsheet))
  contours <- as.contour(DEM)
  writeVector(contours, file, filetype="GPKG", overwrite=TRUE)
}

# load terra library
clusterEvalQ(cl, library(terra))

# Read the mapsheets from external file
mapsheets <- readLines('../mapsheets.txt')

# Give cluster the work to be done
system.time(a<-clusterApply(cl,mapsheets,funtorun))

#Stop cluster
stopCluster(cl)