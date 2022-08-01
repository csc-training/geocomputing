# Geocomputing using CSC resources

This repository contains examples for use of different geospatial applications. Many of the examples are for [CSC supercomputer Puhti](https://docs.csc.fi/computing/systems-puhti/) but may also be helpful for other systems (or your own computer). Please find a list of all geospatial software that is available on Puhti in [CSC docs](https://docs.csc.fi/apps/#geosciences). 

## Examples

### [Gecomputing with R on Puhti](./R/README.md) 

* [puhti](./R/puhti) - serial/array/parallel processing with R on Puhti: Example for calculating contour lines with `terra`, also in parallel with `snow`, `parallel` and `future`
* [raster_predict](./R/raster_predict) - Predicting precence/absence of some species using using `predict()` funcion from `raster` package. Some of the functions in `raster` package support parallel computing and `predict()` is one of these. Includes also the batch job (parallel) file for Puhti.
* [geopackage](./R/geopackage)
* [using R with LiDAR data](./R/R_LiDAR) - examples and exercises
* [how to read and write data to Allas from R](./R/allas)

References for CSC's R spatial tools:
* [Puhti's R for GIS documentation](https://docs.csc.fi/apps/r-env-for-gis/)
* [Puhti's R documentation](https://docs.csc.fi/apps/r-env-singularity/)

### FORCE
* [Examples for using FORCE on Puhti](./force/README.md) 

### GDAL 
* [Serial and parallel using GDAL on Puhti](./gdal/readme.md)

### GRASS 
* [Serial and parallel use of GRASS on Puhti](./grass/readme.md)

### Geospatial Machine Learning course material
* [Overview of exercises](./machineLearning/README.md)

### CSC Notebooks for Geoinformatics setup
* [Example dockerfile](./notebooks/jupyter_geo.dockerfile) for setting up [geospatial Python Jupyter environment](./notebooks/README.md)

### Serial/array/parallel use of PDAL on Puhti
* [Overview](./pdal/README.md) with instructions for PDAL exercises on Puhti

### Pouta 
* [Overview](./pouta/README.md): A collection of instructions to setup virtual machines in [CSC's cPouta environment](https://docs.csc.fi/cloud/pouta/) for different tools:
- [OpenDroneMap as Docker applications](./pouta/docker-applications) - installing other Docker applications would be very similar.
- [GeoServer](./pouta/geoserver) 
- [PostGIS](./pouta/postgis)
- [ArcPy](./pouta/arcpy) 
- [MetaShape](./pouta/metashape_with_VNC) 


### Geocomputing with Python
* [Overview](./python/README.md)
* how to read and write data to Allas from Python with [S3](./python/allas/working_with_allas_from_Python_S3.py) and [swift](./python/allas/working_with_allas_from_Python_Swift.py)
* [Sentinel-1/-2 data download from Finhub and Scihub using sentinelsat](python/sentinel/README.md)
* [Using STAC, xarray and dask for processing satellite images](./python/STAC/stac_xarray_dask_example.ipynb)

#### Puhti 

* [serial/array/parallel processing with Python on Puhti](./python/puhti/README.md)
* [routing](./python/routing/readme.md)
* [serial and parallel zonal statistics calculation](./python/zonal_stats/README.md)
* [geopackage handling in Python](./python/geopackage/README.md)
* [GRASS multiprocessing from Python](./python/grass_multiprocessing_with_python/README.md)

### SNAP
* [Usage of SNAP graph processing tool (gpt) in Puhti](./snap/README.md)


## Scripts

You can download these scripts to any computer using git. To do this, first navigate to the destination folder (in Puhti this could be your project's **projappl** or **scratch** folder):

`cd /projappl/<YOUR-PROJECT>`
or
`cd /scratch/<YOUR-PROJECT>`

And then clone this repository there

`git clone https://github.com/csc-training/geocomputing.git`

## License
These examples are free to use under CC 4.0 BY license. Please acknowledge CSC and Geoportti in your publications, it is important for project continuation and funding reports. As an example, you can write "The authors wish to thank CSC - IT Center for Science, Finland (urn:nbn:fi:research-infras-2016072531) and the Open Geospatial Information Infrastructure for Research (Geoportti, urn:nbn:fi:research-infras-2016072513) for computational resources and support
