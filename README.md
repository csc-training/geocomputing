# Examples for geocomputing using CSC resources

This repository contains examples for:

* Gecomputing with R on Puhti 
  * using R for LiDAR data processing
  * how to read and write data to Allas from R
  * geopackage handling in R
  * serial/array/parallel processing with R on Puhti
* using FORCE on Puhti
* serial and parallel use of gdal on Puhti
* serial and parallel use of GRASS on Puhti
* geospatial Machine Learning course exercises
* example dockerfile for setting up geospatial Python Jupyter environment
* serial/array/parallel use of PDAL on Puhti
* instructions for setting up OpenDroneMap, Geoserver, PostGIS, ArcPy or Metashape on Virtual Machines in CSC Pouta cloud
* Geocomputing with Python on Puhti
  * using STAC, xarray and dask for processing satellite images
  * how to read and write data to Allas from Python
  * geopackage handling in Python
  * GRASS multiprocessing from Python
  * serial/array/parallel processing with Python on Puhti
  * routing on Puhti
  * Sentinel-1/-2 data download from Finhub and Scihub using sentinelsat
  * serial and parallel zonal statistics calculation
* usage of SNAP graph processing tool (gpt) in Puhti

Most examples include batch job scripts for CSC supercomputer Puhti.

If you are interested in setting up cloud environments for GIS see:
- cPouta virtual machines we have some [cPouta GIS examples and instructions](./pouta)
- running containers in [Rahti Containers platform](./rahti)


# Scripts

You can download these scripts to any computer using git. To do this, first navigate to the destination folder (in Puhti this could be your project's **projappl** or **scratch** folder):

`cd /projappl/<YOUR-PROJECT>`
or
`cd /scratch/<YOUR-PROJECT>`

And then clone this repository there

`git clone https://github.com/csc-training/geocomputing.git`

# License
These examples are free to use under CC 4.0 BY license. Please acknowledge CSC and Geoportti in your publications, it is important for project continuation and funding reports. As an example, you can write "The authors wish to thank CSC - IT Center for Science, Finland (urn:nbn:fi:research-infras-2016072531) and the Open Geospatial Information Infrastructure for Research (Geoportti, urn:nbn:fi:research-infras-2016072513) for computational resources and support
