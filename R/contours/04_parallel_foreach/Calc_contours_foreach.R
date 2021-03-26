# This is an spatial analysis example script for using R in CSC Puhti
# This script can be used for parallel jobs.
# The countours are calculated and saved in GeoPackage format.
# The file given as input is a 10m DEM file from Finnish NLS.
# The input files are listed in the mapsheet.txt file

# For parallel tasks the foreach with doMPI is used.
# See https://docs.csc.fi/apps/r-env-singularity/

library(doMPI,quietly=TRUE)
cl<-startMPIcluster()
registerDoMPI(cl)

# Read the mapsheets from external file, in this case from user's workdirectory
mapsheets <- readLines('../mapsheets.txt')

# The function run on each core
# The R modules need to be loaded inside the functions.
# The variables from outside of this function are not visible.

funtorun<-function(mapsheet) {
  DEM <- raster(mapsheet)
  file <- gsub("tif", "gpkg", basename(mapsheet))
  contours<-rasterToContour(DEM)
  writeOGR(contours, dsn = file, layer = "contours", driver = "GPKG", overwrite_layer=TRUE)
}

# Run funtorun function in parallel for each mapsheet. .export passes variables and .packages the necessary packages.
# If return value is used .combine can be used to specify which function to use for combining results.

a<-foreach(i=1:3, .packages=c("raster","rgdal"), .combine="c") %dopar% {
	funtorun(mapsheets[i])
}
#Print combined return values. In this case names of created shapefiles.
print(a)
closeCluster(cl)
mpi.quit()

