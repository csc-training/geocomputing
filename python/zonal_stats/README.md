#Zonal statistics using multiprocessing and virtual raster

In this example zonal statistics are calculated using virtual raster and python multiprocessing library. The idea is that we have multiple zones split across several raster files (and some zones also covering more than one raster) and we want to compute zonal statistics for these zones. The way we handle the multiple raster files in this example is to construct a single virtual raster after which we don't have to worry about which polygon covers which raster. To make processing multiple polygons faster we split the task into ten parts and process them in parallel using multiprocessing library.