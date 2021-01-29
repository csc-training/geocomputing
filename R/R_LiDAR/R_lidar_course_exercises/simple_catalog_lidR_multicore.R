# lidR supports parallel computation of project/catalog. 
# https://rdrr.io/cran/lidR/man/lidR-parallelism.html
# Parallelization is based on chunks. By default 1 chunk = 1 file.
# It is possible to define also chunks smaller than the file. 
# This increases the complexity of calculation and calculation time a little bit.
# But reduces the required memory significantly. 
# The number of workers should be equal or smaller than the number of chunks.
# In this example 4 workers are used.
# All lidR functions support using workers.

library(future)
library("lidR")
#Enabling this will print out a little bit more info about the parallelization plan used.
options(lidR.verbose = TRUE)

# With plan(multicore) the number of workers is based on batch job reservation details.
plan("multicore")

# In Puhti R OpenMP parallelization does not seem to work with lidR, so do not use this option in Puhti. 
# set_lidr_threads(2)

# load catalog
project <- readLAScatalog("/appl/data/geo/mml/laserkeilaus/2008_latest/2019/U442/1/")

# lascheck(ctg_subset)

# output file naming options
opt_output_files(project) <- "batch_output_multicore/dtm_ctg_{XLEFT}_{YBOTTOM}_{ID}"

# NLS lidar files cover 3 x 3 km, so here 1500 x 1500 m chunk size is used -> 4 chunks per file.
opt_chunk_size(project) <- 1500

# summary(ctg_subset)

# Calculate DTM for the catalog, note that the files are written by the catalog itself
# https://rdrr.io/cran/lidR/man/catalog_apply.html
output  <- catalog_sapply(project, grid_terrain, algorithm = tin())