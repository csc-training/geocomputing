# Zonal statistics in parallel for big rasters

In this example zonal statistics are calculated based on a vector polygons from a big raster dataset. 

Here are 2 different code examples for `rasterstats` and `xarrray-spatial` Python libraries.

The data used in the example:
* 10m DEM from NLS
* Field parces from Finnish Food Authority.

The script uses geoconda module in Puhti and reads both datasets directly from [Puhti common GIS data area](https://docs.csc.fi/data/datasets/spatial-data-in-csc-computing-env/#spatial-data-in-puhti).

## Raster data considerations

For handling big rasters 3 main options could be considered:

* **One big file**. 5-10 Gb or even bigger raster files have become rather common. 

* **Virtual raster**, is a GDAL concept to virtually merge rasters that are split to mapsheets. It enables handling many files as if they were one. See [CSC Virtual rasters tutorial](https://docs.csc.fi/support/tutorials/gis/virtual-rasters/) for longer explanation. Creating own virtual rasters is a simple and fast process. Virtual raster is a good solution, if data does not have time dimension. Many of the rester datasets in Puhti common GIS area have virtual rasters added.

* **STAC** enables to find spatial-temporal data and create a datacube of it, inc simple mosaicing. But it requires that the input raster data is available in a STAC API service. A lot of Finnish data is available via [Paituli STAC](https://paituli.csc.fi/stac.html).

### File format
For parallel computing to work well, it is important to use a file format, that supports well partial windowed reading of the data. **Cloud-optimized geotiffs (COG)** are often good for this. This applies for single file, as well for virtual rasters or data from STAC.


## `rasterstats` and `xarrray-spatial` comparision

For the examples here, we use zonal_stats function from [xarrray-spatial](https://xarray-spatial.readthedocs.io/en/stable/user_guide/zonal.html#Zonal-Statistics) and [rasterstats](https://pythonhosted.org/rasterstats/manual.html#zonal-statistics) . These are 2 different libraries, with different features:

| Feature    | `xarrray-spatial` | `rasterstats`
| -------- | ------- | ------- |
| Input vector  | Xarray DataArray  | GeoDataFrame or any Fiona-supported file |
| Input raster | Xarray DataArray | Numpy Array or any GDAL-supported raster file |
| Parellel processing    | Yes, if the Xarray DataArrays are [Dask Arrays](https://docs.xarray.dev/en/stable/user-guide/dask.html)    | Not by default |
| Handle data bigger than the memory? | Yes | No | 

In general `rasterstats` could be the first choice, it:
* works with wider range of data
* does not require data pre-processing,
* it works well, also if the polygons cover only small part of the big raster
* uses less memory than `xarrray-spatial`
* is often faster
* BUT, it is not parallel by default, but here we provide code for parallelization.
  
Use `xarrray-spatial` if you need to handle bigger datasets that do not fit to memory or if the zonal polygons are in raster format originally.

> **_NOTE:_**  If the vector datasets includes a lot of polygons, give the raster data to `rasterstats` as Numpy array, it is much faster then.

### Benchmarking results

The same analysis was done with both libraries, using xxx pixels raster and yy polygons raster.

* `rasterstats` was faster with 1-10 cores.
* `xarrray-spatial` with 40 cores got the fastest Wall time
* `rasterstats` memory usage did not increase with parallelization and was lower than with `xarrray-spatial`
* `xarrray-spatial` memory usage increses with number of cores
  
![image](https://github.com/user-attachments/assets/6d3f2aba-fca2-447c-9e1e-5106c51bcf28)

| Library | Cores | Wall Time (sec) | Compute time (sec) | CPU efficiency (%) | Used memory (Gb)|
| -------- | ------- | ------- | ------- | ------- | ------- |
| `rasterstats` | 1| 565 | 565 | 82 | 4 | 
| `xarrray-spatial` | 1 | 1345 | 1345 | 95 | 6 |
| `rasterstats` | 5| **188** | 421 | 45 | 4 | 
| `xarrray-spatial` | 5 | 355 | 1419 |  80 | 11 |
| `rasterstats` | 10| 183 | 475 | 26 | 4 | 
| `xarrray-spatial` | 10 | 299 | 2189 | 73 | 15 |
| `rasterstats` | 20| 218 | 520 | 12 | 4 | 
| `xarrray-spatial` | 20 | 176 | 2210 | 63 | 20 |
| `xarrray-spatial` | 40 | **130** | 2330 | 45 | 25 |

Detail comments:
* In these tests raster data was given to `rasterstats` as Numpy array, if it was given as file path on disk, the process was very slow - 17965 seconds for similar analysis. 
* `xarrray-spatial` requires the vector data as matching array to the raster data. The vector data was rasterized as a separate first step, it took ~26 seconds. That time is not inlcuded the benchmark results.
* To provide `xarrray-spatial` data as [Dask Arrays](https://docs.xarray.dev/en/stable/user-guide/dask.html), it seemed that currently the only option, is to write rasterized polygons to disk as COG.


