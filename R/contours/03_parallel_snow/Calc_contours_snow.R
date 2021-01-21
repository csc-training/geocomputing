# This is an spatial analysis example script for using R in CSC Puhti
# This scipt can be used for parallel jobs.
# Here 3 .tif files are saved to SagaGIS format
# and then countours are calculated and saved in Shape format.
# The file given as input is a 10m DEM file from Finnish NLS.
# The input files are listed in the mapsheet.txt file

# For parallel tasks the snow package is used.

#Set the names of the folders.
mainDir <- "/scratch/project_2002044/students/training011/R_spatial_exercises/03_parallel_snow"
shapeFolder <- "shape"

# Set the working directory
setwd(mainDir)

#Make folders for files, do not make, if already exist
if (!dir.exists(shapeFolder)) {
  dir.create(shapeFolder)
}

# Start the snow cluster
cl<-getMPIcluster()

# The function run on each core
# The R modules need to be loaded inside the functions.
# The variables from outside of this function are not visible.
funtorun<-function(mapsheet) {
  DEM <- raster(mapsheet)
  shapefile <- file.path(shapeFolder, gsub("tif", "shp", basename(mapsheet)))
  contours<-rasterToContour(DEM)
  shapefile(contours, filename=shapefile, overwrite=TRUE) 
}

# load raster library
clusterEvalQ(cl, library(raster))

#Export variable to each cluster
clusterExport(cl, "mainDir")
clusterExport(cl, "shapeFolder")

#Set working directory
clusterEvalQ(cl, setwd(mainDir))

# Read the mapsheets from external file
mapsheets <- readLines('../mapsheets.txt')

# Give cluster the work to be done
system.time(a<-clusterApply(cl,mapsheets,funtorun))

#Stop cluster
stopCluster(cl)
