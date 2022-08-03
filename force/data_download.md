# Data download with FORCE from Google Cloud on Puhti

PLease also see the great [tutorial in FORCE documentation](https://force-eo.readthedocs.io/en/latest/howto/level1-csd.html#tut-l1csd) for further details.

1. First you need to download the catalogue of the dataset you want to work with: 
On computing node, use the following command to download Sentinel-2B catalogue and store to an existing directory on your projects projappl or scratch directory. 
(Your colleagues with access to this project will be able to use your catalogue as well, no need to download multiple times!)


```
force-level1-csd -u /projappl/project_<your_project_number>/<your_existing_catalogue_directory>
```
This command you may need to run every time before downloading data, to get the newest data integrated into your catalogue.

To download data you will need to authenticate with your google account; if you do not have one, you will need to create one to use this option.

2. Authentication:

```
/appl/opt/google-cloud-sdk/bin/gcloud config set pass_credentials_to_gsutil false

/appl/opt/google-cloud-sdk/bin/gsutil config
```
This prints a long link in terminal which you need to copy to your own computers webbrowser. 
There you will need to login or register your google account and give some rights to gsutil (please make sure to read the text before accepting!)
After accepting a token will be printed on screen which needs to be copied back to Puhti terminal.
This creates your credentials file in `/users/<userrname>/.boto` (if not, please make sure you ran the gcloud config set command before gsutil config!)

3. Start downloading data

The example call below will download all data of sensor Sentinel-2B with 0-10% cloudcover between the dates of 1.July'22 and 31.July'22 of tile T35VM. 
Instead of the tile, also a shapefile or Polygon coordinates can be given, please see the [FORCE level1-csd tutorial](https://force-eo.readthedocs.io/en/latest/howto/level1-csd.html#tut-l1csd) for more information.
To check how much data will be downloaded before starting the download you can add `-n` flag to below call:

```
force-level1-csd -s S2B -c 0,10 -d 20220701,20220731 /scratch/project_<your_project_number>/<your_existing_catalogue_directory>  /scratch/project_<your_project_number>/<your_existing_data_directory> x T35VM
```
-> downloads one file (directories have to exist!)
