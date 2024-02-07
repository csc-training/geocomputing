# Downloading data from Copernicus Data Space Ecosystem

The [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) (CDSE) provides multiple ways of querying and downloading data. Check out the [CSC Earth Observation guide](https://docs.csc.fi/support/tutorials/gis/eo_guide) for further information about the CDSE.

## CDSE S3 download with rclone
This example shows how find and to copy data from CDSE S3 object storage using `rclone`. 

The script [CDSE_S3_download.sh](CDSE_S3_download.sh) provides an example on how to query and download CDSE with `rclone` command line tool:

1. Query CDSE Sentinel-2 catalog based on startdate, enddate, cloudcover and tilename using [openSearch API](https://documentation.dataspace.copernicus.eu/APIs/OpenSearch.html)
2. Download the found data from CDSE object storage via `s3` using `rclone`. Data can be downloaded to local disk or directly to CSC's object storage Allas. 

To run the script, first **connection details** to must be set up.

1. [Get secret and access keys for CDSE](https://documentation.dataspace.copernicus.eu/APIs/S3.html#generate-secrets).
2. Configure rclone to use CDSE.
    * [General rclone configuration instructions](https://rclone.org/docs/#configure)
    * For most settings CDSE can use the same as Allas, see [Allas rclone settings](https://docs.csc.fi/data/Allas/using_allas/rclone_local/#configuring-s3-connection-in-windows)
    * CDSE endpoint: `eodata.dataspace.copernicus.eu`.
    * Name of the remote: `cdse`
3. If you want to download files to your local disk, you are ready to go. 
4. If you want to copy files to another object storage, for example CSC Allas, then set up `rclone` connection details also for the second service. Follow [Allas: Copying files directly between object storages](https://docs.csc.fi/data/Allas/accessing_allas/#copying-files-directly-between-object-storages) instructions. In this example `s3allas` is the name of the second remote connection.

The script should work on any Linux/Mac machine that has `rclone` installed. In CSC supercomputers, `rclone` is included in the `allas`-module.

## Direct use of S3 data with GDAL, Python and R
CDSE S3 data can also be used directly with [GDAL-based tools, inc Python, R and QGIS](https://docs.csc.fi/support/tutorials/gis/gdal_cloud/#vsis3-reading-and-writing-files-fromto-s3-services).
