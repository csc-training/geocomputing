library("lidR")
# load catalog
library(future)
# set the number of cores accordingly to your available cpus (e.g. your request to Puhti)
# Note the way have defining this has changed from lidR 2.10
# https://github.com/Jean-Romain/lidR/blob/master/NEWS_v2.md
plan(multisession , workers = 16)
#opt_cores(ctg_subset) <- 16

ctg_subset <- catalog("las_files.txt")
# lascheck(ctg_subset)
# computation options
outdir <- "batch_output"
opt_output_files(ctg_subset) <- paste0("./", outdir, "/dtm_ctg_{XLEFT}_{YBOTTOM}_{ID}")
# Internal engine will sequentially process chunks of size 100 x 100 m 
opt_chunk_size(ctg_subset) <- 100

# summary(ctg_subset)

# Calculate DTM for the catalog, note that the files are written by the catalog itself
# and that a virtual raster is created with name grid_terrain.vrt
dtm <- grid_terrain(ctg_subset, algorithm = tin())
