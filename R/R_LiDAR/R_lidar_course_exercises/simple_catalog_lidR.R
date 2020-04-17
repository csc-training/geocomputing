library("lidR")
# load catalog
ctg_subset <- catalog("las_files.txt")
# lascheck(ctg_subset)
# computation options
outdir <- "batch_output"
opt_output_files(ctg_subset) <- paste0("./", outdir, "/dtm_ctg_{XLEFT}_{YBOTTOM}_{ID}")
opt_chunk_size(ctg_subset) <- 100
# set the number of cores accordingly to your available cpus (e.g. your request to Puhti)
opt_cores(ctg_subset) <- 16

# summary(ctg_subset)


# Calculate DTM for the catalog, note that the files are written by the catalog itself
# and that a virtual raster is created with name grid_terrain.vrt
dtm <- grid_terrain(ctg_subset, algorithm = tin())
