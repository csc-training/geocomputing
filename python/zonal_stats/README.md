# Zonal statistics in parallel for big rasters

In this example zonal statistics are calculated based on a vector polygons from a big raster dataset. 

Here are three different code examples for calculating zonal statiscis in parallel with `rasterstats` or `xarrray-spatial` Python libraries:
* One raster and a lot of polygons. For parallelization the the polygons are split to batches. `rasterstats` + `multiprocessing`
* Several rasters (different dates and bands). The statistics for each raster are cacluated in parallel. `rasterstats` + `dask` delayed functions
* `Xarray-spatial` has built-in parallelization, it splits the raster to chunks using `Dask DataArrays`.

The data used in the example:
* 10m DEM from NLS (or Sentinel-2 11-day data mosaics from STAC)
* Field parces from Finnish Food Authority.

The script uses geoconda module in Puhti and reads both datasets directly from [Puhti common GIS data area](https://docs.csc.fi/data/datasets/spatial-data-in-csc-computing-env/#spatial-data-in-puhti). Alternative public HTTPS-links for data are also given.

## `rasterstats` and `xarrray-spatial` comparision

For the examples here, we use zonal_stats function from [xarrray-spatial](https://xarray-spatial.readthedocs.io/en/stable/user_guide/zonal.html#Zonal-Statistics) and [rasterstats](https://pythonhosted.org/rasterstats/manual.html#zonal-statistics) . These are 2 different libraries, with different features:

| Feature    | `xarrray-spatial` | `rasterstats`
| -------- | ------- | ------- |
| Input vector  | Xarray DataArray  | GeoDataFrame or any Fiona-supported file |
| Input raster | 2D Xarray DataArray | 2D Numpy Array or any GDAL-supported raster file |
| Parellel processing    | Yes, if the Xarray DataArrays are [Dask Arrays](https://docs.xarray.dev/en/stable/user-guide/dask.html)    | Not by default |
| Handle data bigger than the memory? | Yes | Not by default | 

In general `rasterstats` could be the first choice, it:
* works with wider range of data
* does not require data pre-processing,
* it works well, also if the polygons cover only small part of the big raster
* uses less memory than `xarrray-spatial`
* is often faster
* it is not parallel by default, but here we provide here code for parallelization.
  
Use `xarrray-spatial` if you need to handle bigger datasets, which do not fit to memory or if the zonal polygons are in raster format originally.


### Benchmarking results

The same analysis was done with both libraries, using 20 000 x 20 000 pixels DEM raster and 195 000 field polygons.

Key findings:
* `rasterstats` was faster with 1-10 cores.
* Using ~5 cores seems to be optimal for `rasterstats`.
* `xarrray-spatial` benefits more for cores, with 40 cores it got the fastest Wall time, also compared to 'rasterstats'
* `rasterstats` memory usage did not increase with parallelization and was lower than with `xarrray-spatial`
* `xarrray-spatial` memory usage increses with number of cores
  
![image](https://github.com/user-attachments/assets/6d3f2aba-fca2-447c-9e1e-5106c51bcf28)

| Library | Cores | Wall Time (sec) | Compute time (sec) | CPU efficiency (%) | Used memory (Gb)|
| -------- | ------- | ------- | ------- | ------- | ------- |
| `rasterstats` | 1| 565 | 565 | 82 | 4 | 
| `xarrray-spatial` | 1 | 1 345 | 1 345 | 95 | 6 |
| `rasterstats` | 5| **188** | 421 | 45 | 4 | 
| `xarrray-spatial` | 5 | 355 | 1 419 |  80 | 11 |
| `rasterstats` | 10| 183 | 475 | 26 | 4 | 
| `xarrray-spatial` | 10 | 299 | 2 189 | 73 | 15 |
| `rasterstats` | 20| 218 | 520 | 12 | 4 | 
| `xarrray-spatial` | 20 | 176 | 2 210 | 63 | 20 |
| `xarrray-spatial` | 40 | **130** | 2 330 | 45 | 25 |

Details:
* In these tests, raster data was given to `rasterstats` as Numpy array. Giveng the raster data as file path on disk was tested only with 1 core, but the process was very slow - 17 965 seconds. 
* `xarrray-spatial` requires the vector data as matching array to the raster data. The vector data was rasterized as a separate first step, it took ~26 seconds. That time is not inlcuded the benchmark results.
* Joining statistics back to the geodataframe was left out from the tests, because that would be a serial process and would increase time for all scenarios in a similar way.

## Raster data considerations

For handling big rasters 3 main options could be considered:

* **One big file**. 5-10 Gb or even bigger raster files have become rather common. 

* **Virtual raster**, is a GDAL concept to virtually merge rasters that are split to mapsheets. It enables handling many files as if they were one. See [CSC Virtual rasters tutorial](https://docs.csc.fi/support/tutorials/gis/virtual-rasters/) for longer explanation. Creating own virtual rasters is a simple and fast process. Virtual raster is a good solution, if data does not have time dimension. Many of the raster datasets in Puhti common GIS area have virtual rasters added.

* **STAC** enables to find spatial-temporal data and create a datacube of it, inc simple mosaicing. But it requires that the input raster data is available via STAC. A lot of Finnish data is available via [Paituli STAC](https://paituli.csc.fi/stac.html). 

### File format
* For parallel computing to work well, it is important to use a file format, that supports well partial windowed reading of the data. **Cloud-optimized geotiffs (COG)** are often good for this. This applies for single file, as well for virtual rasters or data from STAC.
* If your raster data is in JPEG2000 format or other format, which does not well suite parallel reads, condsider using `rasterstats` so that the whole dataset is read at once.

### Reading rasters to `rasterstats`

* If the vector datasets includes a lot of polygons, give the raster data to `rasterstats` as Numpy array, it is much faster then.
* If the vector datasets includes a few polygons polygons, that cover small part of the raster, it might be better not to read all raster data to memory and give to zonal_stats function the path to the file.
* To read data from a single file or virtual raster, use `rasterio` as shown in the example.
* To read data from STAC:
  * If interested in statics from several files, found with STAC, see the rastestats and STAC example to analyze rasters in parallel.
  * If interested only in 1 or few files:
     * Query STAC for data and create an Xarray DataArray of it as show in [CSC STAC exampes](../STAC). In the example the resulting `monthly` DataArray has size: time: 2, y: 601, x: 601, band: 5.
     * Select 2D DataArray from datacube. Keep one band from one timestep.
     * Convert the Xarray DataArray to Numpy array. This also reads the data to memory.

```
date1 = monthly. monthly.sel(band='b04').sel(time='2021-08-01T00:00:00.000000000')
date1_numpy = date1_transposed.compute().data
```

### Reading rasters to `xarrray-spatial`
* `xarrray-spatial` uses raster data from Xarray Arrays, use `rioxarray` to read single file or virtual raster as shown in the example.
* To provide `xarrray-spatial` vector data as [Dask Arrays](https://docs.xarray.dev/en/stable/user-guide/dask.html), it seemed that currently the only option, is to write rasterized polygons to disk as Cloud-optimized geotiff (COG). And then read them with `rioxarray`.
* To read data from STAC, follow the same steps as described for `rasterstats`, but leave out the last step of converting to Numpy. In this way `date1_transposed` is lazyly loaded DataArray and no data is read to memory yet. `xarrray-spatial` will fetch data it is processing it.

```
date1 = monthly. monthly.sel(band='b04').sel(time='2021-08-01T00:00:00.000000000')
```
