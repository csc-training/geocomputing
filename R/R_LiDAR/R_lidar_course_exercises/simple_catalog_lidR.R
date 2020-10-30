library("lidR")
#Enabling this will print out a little bit more info about the parallelization plan used.
options(lidR.verbose = TRUE)
# load catalog
library(future)
# set the number of cores accordingly to your available cpus (e.g. your request to Puhti)


# https://rdrr.io/cran/lidR/man/lidR-parallelism.html
# Use 4 workers, each with 2 threads.
# Workers are used for catalog_sapply files / chunks
# All lidR functions support using workers.
plan(multisession , workers = 4)

# Threads are used for functions supporting OpenMP parallelization 
# Only some functions support using OpenMP parallelization
# Check lidR-parallelism.html page how to see which functions support OpenMP.
# grid_terrain function actually does not seem to benefit from OpenMP threads, used here only as example
# Remember to match with OMP_NUM_THREADS in the batch job file. 
set_lidr_threads(2)

# Note the way have defining this has changed from lidR 2.10, earlier it was
# opt_cores(ctg_subset) <- 4
# https://github.com/Jean-Romain/lidR/blob/master/NEWS_v2.md

#project <- readLAScatalog('/appl/data/geo/mml/laserkeilaus/2008_latest/2019/U442/1/U4422H2.laz')
project <- readLAScatalog("/appl/data/geo/mml/laserkeilaus/2008_latest/2019/U442/1/")
# lascheck(ctg_subset)
# computation options
outdir <- "batch_output"
opt_output_files(project) <- paste0("./", outdir, "/dtm_ctg_{XLEFT}_{YBOTTOM}_{ID}")
# Internal engine could sequentially process chunks of size 1000 x 1000 m 
# Be careful with this, with a lot of files it likely only causes unnecceary overhead to chunk one file internally,
# therefore commented out here. 
# opt_chunk_size(project) <- 1000

# summary(ctg_subset)

# Calculate DTM for the catalog, note that the files are written by the catalog itself
# https://rdrr.io/cran/lidR/man/catalog_apply.html
output  <- catalog_sapply(project, grid_terrain, algorithm = tin())
writeRaster(output, 'dem.tif', format="GTiff", overwrite=TRUE)
