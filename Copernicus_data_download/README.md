# Downloading data from Copernicus Data Space Ecosystem

The [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) (CDSE) provides multiple ways of querying and downloading data. Check out the [CSC Earth Observation guide](https://docs.csc.fi/support/tutorials/gis/eo_guide) for further information about the CDSE.

## S3 download with rclone
This example shows how to copy data from CDSE object storage directly to CSC's object storage Allas using `S3`. 

1. [Get secret and access keys for CDSE](https://documentation.dataspace.copernicus.eu/APIs/S3.html#generate-secrets).
2. Set up your `rclone` connection details for both services, follow [Allas: Copying files directly between object storages](https://docs.csc.fi/data/Allas/accessing_allas/#copying-files-directly-between-object-storages) instructions. CDSE endpoint is `eodata.dataspace.copernicus.eu`.
3. The script [CDSE_to_Allas_object_storage.sh](CDSE_to_Allas_object_storage.sh) provides an example on how to query and download CDSE with command line tools.

## Direct use of S3 data with GDAL, Python and R
CDSE is technically similar to CSC Allas, so it is possible to use data from there also directly with [GDAL-based tools, inc Python, R and QGIS](https://docs.csc.fi/support/tutorials/gis/gdal_cloud/#vsis3-reading-and-writing-files-fromto-s3-services).
