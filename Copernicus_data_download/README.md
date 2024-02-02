# Downloading data from Copernicus Data Space Ecosystem

The Copernicus Data Space Ecosystem (CDSE) provides multiple ways of querying and downloading data. 

Using `s3` access, you can copy data from CDSE object storage also directly to CSCs object storage Allas, following the instructions for setting up `rclone on [Allas documentation page](https://docs.csc.fi/data/Allas/accessing_allas/#copying-files-directly-between-object-storages) with endpoint `eodata.dataspace.copernicus.eu` and secret and access keys from following the [instructions about generating CDSE access keys](https://documentation.dataspace.copernicus.eu/APIs/S3.html#generate-secrets). 

The script [CDSE_to_Allas_object_storage.sh](CDSE_to_Allas_object_storage.sh) provides an example on how to query and download CDSE with command line tools.

You can also use `boto3` with  Python, for which you can find an example here :[Python Allas S3 example](../python/allas/working_with_allas_from_Python_S3.py).

Check out the [CSC Earth Observation guide](https://docs.csc.fi/support/tutorials/gis/eo_guide) for further information about the CDSE.
