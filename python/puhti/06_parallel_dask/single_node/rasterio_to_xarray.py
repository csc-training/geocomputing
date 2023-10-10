import rasterio
import xarray as xr
import numpy as np
import pandas as pd
import os


def rasterio_to_xarray(fname):
    """Converts the given file to an xarray.DataArray object.

    Arguments:
     - `fname`: the filename of the rasterio-compatible file to read

    Returns:
        An xarray.DataArray object containing the data from the given file,
        along with the relevant geographic metadata.

    Notes:
    This produces an xarray.DataArray object with two dimensions: x and y.
    The co-ordinates for these dimensions are set based on the geographic
    reference defined in the original file.

    This has only been tested with GeoTIFF files: use other types of files
    at your own risk!"""
    with rasterio.drivers():
        with rasterio.open(fname) as src:
            data = src.read(1)

            # Set values to nan wherever they are equal to the nodata
            # value defined in the input file
            data = np.where(data == src.nodata, np.nan, data)

            # Get coords
            nx, ny = src.width, src.height
            x0, y0 = src.bounds.left, src.bounds.top
            dx, dy = src.res[0], -src.res[1]

            coords = {
                "y": np.arange(start=y0, stop=(y0 + ny * dy), step=dy),
                "x": np.arange(start=x0, stop=(x0 + nx * dx), step=dx),
            }

            dims = ("y", "x")

            attrs = {}

            try:
                aff = src.affine
                attrs["affine"] = aff.to_gdal()
            except AttributeError:
                pass

            try:
                c = src.crs
                attrs["crs"] = c.to_string()
            except AttributeError:
                pass

    return xr.DataArray(data, dims=dims, coords=coords, attrs=attrs)


def xarray_to_rasterio(xa, output_filename):
    """Converts the given xarray.DataArray object to a raster output file
    using rasterio.

    Arguments:
     - `xa`: The xarray.DataArray to convert
     - `output_filename`: the filename to store the output GeoTIFF file in

    Notes:
    Converts the given xarray.DataArray to a GeoTIFF output file using rasterio.

    This function only supports 2D or 3D DataArrays, and GeoTIFF output.

    The input DataArray must have attributes (stored as xa.attrs) specifying
    geographic metadata, or the output will have _no_ geographic information.

    If the DataArray uses dask as the storage backend then this function will
    force a load of the raw data.
    """
    # Forcibly compute the data, to ensure that all of the metadata is
    # the same as the actual data (ie. dtypes are the same etc)
    xa = xa.load()

    if len(xa.shape) == 2:
        count = 1
        height = xa.shape[0]
        width = xa.shape[1]
        band_indicies = 1
    else:
        count = xa.shape[0]
        height = xa.shape[1]
        width = xa.shape[2]
        band_indicies = np.arange(count) + 1

    processed_attrs = {}

    try:
        val = xa.attrs["affine"]
        processed_attrs["affine"] = rasterio.Affine.from_gdal(*val)
    except KeyError:
        pass

    try:
        val = xa.attrs["crs"]
        processed_attrs["crs"] = rasterio.crs.CRS.from_string(val)
    except KeyError:
        pass

    with rasterio.open(
        output_filename,
        "w",
        driver="GTiff",
        height=height,
        width=width,
        dtype=str(xa.dtype),
        count=count,
        **processed_attrs
    ) as dst:
        dst.write(xa.values, band_indicies)


def xarray_to_rasterio_by_band(xa, output_basename, dim="time", date_format="%Y-%m-%d"):
    for i in range(len(xa[dim])):
        args = {dim: i}
        data = xa.isel(**args)
        index_value = data[dim].values

        if type(index_value) is np.datetime64:
            formatted_index = pd.to_datetime(index_value).strftime(date_format)
        else:
            formatted_index = str(index_value)

        filename = output_basename + formatted_index + ".tif"
        xarray_to_rasterio(data, filename)
        print("Exported %s" % formatted_index)
