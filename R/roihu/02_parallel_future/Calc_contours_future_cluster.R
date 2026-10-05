# This is an spatial analysis example script for using R in CSC Roihu
# This script can be used for parallel jobs.
# The countours are calculated and saved in GeoPackage format.
# The file given as input is a 10m DEM file from Finnish NLS.
# The input files are listed in the mapsheet.txt file

# For parallel tasks future package is used.

start <- Sys.time()

# load libraries
library(furrr)
library(terra)

# Start the snow cluster and create a plan with future package
cl<-getMPIcluster()
plan(cluster, workers = cl)

# The function run on each core
funtorun <- function(mapsheet) {
  DEM <- terra::rast(mapsheet)
  file <- gsub("\\.tif", ".gpkg", basename(mapsheet))
  contours <- terra::as.contour(DEM)
  terra::writeVector(contours, file, filetype="GPKG", overwrite=TRUE)
}

# Read the mapsheets from external file
mapsheets <- readLines('../mapsheets.txt')

# Give cluster the work to be done
a<-future_map(mapsheets,funtorun, .options = furrr_options(seed = TRUE))

# Print handled files
cat(sprintf("Wrote %d files\n", length(a)))

#Stop cluster
stopCluster(cl)

end <- Sys.time()
cat(sprintf("Script completed in %.1f seconds\n", as.numeric(difftime(end, start, units = "secs"))))


