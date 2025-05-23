# Geocomputing using CSC resources

This repository contains examples for use of different geospatial applications. Many of the examples are for [CSC supercomputer Puhti](https://docs.csc.fi/computing/systems-puhti/) but may also be helpful for other systems (or your own computer). Please find a list of all geospatial software that is available on Puhti in [CSC docs](https://docs.csc.fi/apps/#geosciences). 

## Puhti

### R
* [Overview](./R/README.md)
* [Puhti](./R/puhti) - serial/array/parallel processing with R.
* [R for LiDAR data](./R/R_LiDAR): lidR and rlas
* [Working with Allas data from R](./R/allas)
* [Reading NLS topographic database geopackage with R](./R/geopackage)


### Python
* [Overview](./python/README.md)
* [Puhti](./Python/puhti/README.md) - serial/array/parallel processing with Python.
* [Working with Allas data from Python](./Python/allas)
* [Reading NLS topographic database geopackage with Python](./python/geopackage/README.md)
* [GRASS multiprocessing from Python](./python/grass_multiprocessing_with_python/README.md)
* [Routing](./python/routing/readme.md)
* [Sentinel data download from Finhub using sentinelsat](python/sentinel/README.md)
* [STAC, xarray and dask for downloading and processing data](./python/STAC/stac_xarray_dask_example.ipynb)
* [Zonal statistics in parallel](./python/zonal_stats/README.md)
* [Python Dask-geopandas](./python/dask_geopandas/README.md)

### Other tools
* [FORCE ](./force/README.md)  
* [GDAL](./gdal/readme.md)
* [GRASS](./grass/readme.md)
* [PDAL](./pdal/README.md) 
* [SNAP graph processing tool gpt](./snap/README.md)

### Use cases / longer examples
* [GeoPortti share Github repository](https://github.com/geoporttishare?tab=repositories) includes several longer examples of HPC usage.

## Pouta 
* [Instructions to setup geospatial tools](./pouta/README.md) to virtual machines in [CSC's cPouta environment](https://docs.csc.fi/cloud/pouta/), inc OpenDroneMap, GeoServer, ArcPy and MetaShape.

## CSC Notebooks
* [Setting up geospatial Python Jupyter environment](./noppe/Readme.md)

## Download

If you have installed Git or You can download these scripts to any computer using git. To do this, first navigate to the destination folder (in Puhti this could be your project's **projappl** or **scratch** folder):

`cd /projappl/<YOUR-PROJECT>`
or
`cd /scratch/<YOUR-PROJECT>`

And then clone this repository there

`git clone https://github.com/csc-training/geocomputing.git`

If Git is not available, you can download the files also as zip-file from the `Code` drop-down menu above.


## License
These examples are free to use under CC 4.0 BY license unless marked otherwise.

## Acknowledgement

Please acknowledge CSC and Geoportti in your publications, it is important for project continuation and funding reports. As an example, you can write "The authors wish to thank CSC - IT Center for Science, Finland (urn:nbn:fi:research-infras-2016072531) and the Open Geospatial Information Infrastructure for Research (Geoportti, urn:nbn:fi:research-infras-2016072513) for computational resources and support
