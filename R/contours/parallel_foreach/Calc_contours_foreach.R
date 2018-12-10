# This is an spatial analysis example script for using R in CSC Taito
# This script can be used for parallel jobs.
# Here 3 .tif files are saved to SagaGIS format
# and then countours are calculated and saved in Shape format.
# The file given as input is a 10m DEM file from Finnish NLS.
# The input files are listed in the mapsheet.txt file

# For parallel tasks the foreach with doMPI is used.
# See https://research.csc.fi/-/r

library(doMPI,quietly=TRUE)
cl<-startMPIcluster()
registerDoMPI(cl)

#Set directory for output files (in this case from user's workdirectory): 
mainDir <- file.path(Sys.getenv("WRKDIR"), "R_contours_foreach")
gridFolder <- file.path(mainDir, "1_grid")
shapeFolder <- file.path(mainDir, "2_shape")

# Read the mapsheets from external file, in this case from user's workdirectory
mapsheets <- readLines(file.path(Sys.getenv("WRKDIR"),'geocomputing/R/contours/mapsheets.txt'))


# Set the working directory
if (!dir.exists(mainDir)) {
  dir.create(mainDir)
}

#Make folders for files, do not make, if already exist
if (!dir.exists(shapeFolder)) {
  dir.create(shapeFolder)
}

if (!dir.exists(gridFolder)) {
  dir.create(gridFolder)
}

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

  return(shapefile)
  #The tool gives like other RSAGA tools "Error: select a tool" message, but it actually is working :)
}

# Run funtorun function in parallel for each mapsheet. .export passes variables and .packages the necessary packages.
# If return value is used .combine can be used to specify which function to use for combining results.

a<-foreach(i=1:3, .export=c("gridFolder", "shapeFolder"), .packages=c("RSAGA","gdalUtils"), .combine="c") %dopar% {
	funtorun(mapsheets[i])
}
#Print combined return values. In this case names of created shapefiles.
print(a)
closeCluster(cl)
mpi.quit()

