### Sentinel download script

This script is an example how to find and download large quantities of Sentinel-2 images using Python and the [sentinelsat library](https://sentinelsat.readthedocs.io).

The script favors the Finnish **Finhub API** over the European **Scihub API** if the same image is found from both. 

Another option for similar task is to use [STAC ](../STAC).
 
### Running
On local computer just install the sentinelsat library first.

In Puhti sentinelsat is included in the [geoconda module](https://docs.csc.fi/apps/geoconda/), which must be loaded before running the script.

```
module load geoconda
python sentinelsat_download_from_finhub_and_scihub.py
```

You can run the script simply on login-node for smaller amounts of data.

For bigger amounts of data you can use [screen](https://linuxize.com/post/how-to-use-linux-screen/) or [interactive session](https://docs.csc.fi/computing/running/interactive-usage/).

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
