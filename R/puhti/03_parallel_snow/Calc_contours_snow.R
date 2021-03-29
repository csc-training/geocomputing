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
  DEM <- raster(mapsheet)
  file <- gsub("tif", "gpkg", basename(mapsheet))
  contours<-rasterToContour(DEM)
  writeOGR(contours, dsn = file, layer = "contours", driver = "GPKG", overwrite_layer=TRUE)
}

# load raster library
clusterEvalQ(cl, library(raster))
clusterEvalQ(cl, library(rgdal))

# Read the mapsheets from external file
mapsheets <- readLines('../mapsheets.txt')

# Give cluster the work to be done
system.time(a<-clusterApply(cl,mapsheets,funtorun))

#Stop cluster
stopCluster(cl)