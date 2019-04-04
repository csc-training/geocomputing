#Read the command line argument, which is the path to a las file.
args = commandArgs(trailingOnly=TRUE)
#Gets las_name from argument
if (length(args)==0) {
  stop("Please give a las file name.", call.=FALSE)
} else if (length(args)==1) {
  # input file
  las_name <- args[1]
}


library("lidR")
print(las_name)

# name with tif extension
out_name <- paste0("dtm_", tools::file_path_sans_ext(basename(las_name)),".tif")

# Open las file
las <- readLAS(las_name)
print(las)
# Calculate DTM and save to disk
dtm <- grid_terrain(las, algorithm = tin())
writeRaster(dtm, paste0("array_output/", out_name), format="GTiff", overwrite=TRUE)
