
# Parallel processing of Sentinel images with Dask and Xarray in CSC environment

## NDVI calculation with S2 L2 images

The script iterates over Sentinel image folders (.SAFE folders) and calculates NDVI using xarray and utilizes also parallel calculation with Dask. This uses delayed functions https://docs.dask.org/en/latest/delayed.html which means the library maps first everything that needs to be ran, finds what resources are available (automatically) and distributes the work load in the most efficient way.

### ndvi_dask_example.py

This is the main script that reads images, calculates ndvi and saves the results

### rasterio_to_xarray.py

As dask and xarray are not yet capable of saving to GeoTiffs this example uses this help script downloaded from here
https://github.com/robintw/XArrayAndRasterio/blob/master/rasterio_to_xarray.py

### ndvi_dast_example.sh

The simple batch job file used to test this. Change the parameters accordingly! Project, partition etc. The script was tested with relative small amount of 7 Sentinel images. Benchmarking suggested that number of cpu cores should be at minimum the number of Sentinel images. Dask knows how to divide pixels to chunks so several CPUs can work on one image. Though on Puhti, the maximum number of CPUs is 40 as this kind of Python processes can't run on several nodes.

## Benchmark

| Number of CPU cores | seconds |
|---------------------|---------|
| 1                   | 439     |
| 2                   | 230     |
| 4                   | 133     |
| 6                   | 100     |
| 8                   | 93      |
| 10                  | 83      |
| 12                  | 78      |
| 16                  | 67      |

### More information

https://docs.dask.org/en/latest/
http://xarray.pydata.org/en/stable/dask.html
https://examples.dask.org/xarray.html
