# Zonal statistics in parallel for big rasters

In this example zonal statistics are calculated based on a vector polygons from a big raster dataset. 

The data used in the example:
* 10m DEM from NLS
* Field parces from Finnish Food Authority.

The script uses geoconda module in Puhti and reads both datasets directly from [Puhti common GIS data area](https://docs.csc.fi/data/datasets/spatial-data-in-csc-computing-env/#spatial-data-in-puhti).

## Raster data considerations

For handling big rasters 3 main options could be considered:

* **One big file**. 5-10 Gb or even bigger raster files have become rather common. 

* **Virtual raster**, is a GDAL concept to virtually merge rasters that are split to mapsheets. It enables handling many files as if they were one. See [CSC Virtual rasters tutorial](https://docs.csc.fi/support/tutorials/gis/virtual-rasters/) for longer explanation. Creating own virtual rasters is a simple and fast process. Virtual raster is a good solution, if data does not have time dimension.

* **STAC** enables to find spatial-temporal data and create a datacube of it, inc simple mosaicing. But it requires that the input raster data is available in a STAC API service. A lot of Finnish data is available via [Paituli STAC](https://paituli.csc.fi/stac.html).

### File format
For parallel computing to work, it is important to use a file format, that supports well partial windowed reading of the data. **Cloud-optimized geotiffs (COG)** are often good for this.


## Example solutions

Here we provide two solutions, using `xarrray-spatial` [zonal_stats](https://xarray-spatial.readthedocs.io/en/stable/user_guide/zonal.html#Zonal-Statistics) and `rasterstats` [zonal_stats](https://pythonhosted.org/rasterstats/manual.html#zonal-statistics) . In general `rasterstats` works with wider range of data and does not require data pre-processing, but `xarrray-spatial` can handle bigger datasets. `rasterstats` might also be better choice if the polygons cover only small part of the raster.

| Feature    | `xarrray-spatial` | `rasterstats`
| -------- | ------- | ------- |
| Input vector  | Xarray DataArray, matching the raster data, so the vector data has to be rasterized as a first step.    | GeoDataFrame or any Fiona-supported file |
| Input raster | Xarray DataArray | Numpy Array or any GDAL-supported raster file |
| Parellel processing    | Yes, if the Xarray DataArrays are [Dask Arrays](https://docs.xarray.dev/en/stable/user-guide/dask.html)    | No, but in the example here is shown how it can be used in parallel with some extra code using for example `multiprocessing` library. |
| Is it possible to handle data that does not fit to the memory? | Yes | No | 



