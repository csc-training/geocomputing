library("lidR")
# load catalog
library(future)
# set the number of cores accordingly to your available cpus (e.g. your request to Puhti)
# Note the way have defining this has changed from lidR 2.10
# https://github.com/Jean-Romain/lidR/blob/master/NEWS_v2.md
plan(multisession , workers = 16)
#opt_cores(ctg_subset) <- 16

#project <- readLAScatalog('/appl/data/geo/mml/laserkeilaus/2008_latest/2019/U442/1/U4422H2.laz')
project <- readLAScatalog("/appl/data/geo/mml/laserkeilaus/2008_latest/2019/U442/1/")
# lascheck(ctg_subset)
# computation options
outdir <- "batch_output"
opt_output_files(project) <- paste0("./", outdir, "/dtm_ctg_{XLEFT}_{YBOTTOM}_{ID}")
# Internal engine will sequentially process chunks of size 100 x 100 m 
opt_chunk_size(project) <- 100

# summary(ctg_subset)

# Calculate DTM for the catalog, note that the files are written by the catalog itself
output  <- catalog_sapply(project, grid_terrain, algorithm = tin())
writeRaster(output, 'dem.tif', format="GTiff", overwrite=TRUE)
