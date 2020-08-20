### Sentinel download script

This script is an example how to find and download large quantities of Sentinel-2 images using Python and the sentinelsat library.

The script favors the Finnish **Finhub API** over the European **Scihub API** if the same image is found from both. 

### Running

You can run this in an interactive session that can be started from the login node with

`sinteractive -i`
`module load geoconda`
`python sentinelsat_download_from_finhub_and_scihub.py`

or you can make a batch job file and run it with a batch job

### Unzipping 

As the Python unzipping is a little complicated with files over 1GB, we recommend using bash commands to unzip the files

Unzip all files to the current directory
`unzip '*.zip`

Unzip all files to current directory and delete them at the same time
`find . -depth -name '*.zip' -execdir unzip -n {} \; -delete`

## Things to consider 

* Finhub API has only L1C images
* If the images are over a year old, they move to Long Term Archive in Scihub. This script can't download them. [More information](https://scihub.copernicus.eu/userguide/LongTermArchive)
* If the area of interest is in the middle of two UTM zones, the script often downloads the same image in two different projections. You can specify the UTM zone if you do not want to download duplicates