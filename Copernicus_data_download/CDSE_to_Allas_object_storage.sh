#!/bin/bash

###############
# Example script to 
# 1. Query Copernicus Data Space Ecosystem Sentinel-2 catalog based on startdate, enddate, cloudcover and tilename using [openSearch API](https://documentation.dataspace.copernicus.eu/APIs/OpenSearch.html)
# 2. Download the found data from CDSE object storage to Allas object storage
#
# Requirements: Rclone setup to work with allas as [s3allas] (s3 setup connected to CSC project for Allas) and CDSE as [cdse].
# See [CSC EO guide](https://docs.csc.fi/support/tutorials/gis/eo_guide/) about how to set it up. 
# Instead of downloading directly to Allas, data can also be downloaded to a computing environment via [s3cmd](https://docs.csc.fi/data/Allas/using_allas/s3_client/). 
#
# Based on script provided by Maria Yli-Heikkilä (LUKE) - adapted to CDSE by Samantha Wittke, CSC - IT center for Science

# Provide Sentinel-2 tilenames that you want to download
TILES=("T34VDM" "T34VEM" "T34VEN")

# Provide your bucketname for Allas; bucketname is then constructed: BUCKETBASENAME-YEAR-TILE
BUCKETBASENAME="your_bucket_name"

# Provide the timedelta - start date and time
STARTDATE=2023-05-01T00:00:00

# end date and time ; fixed or set to current date
#CURRENTDATE=$(date +"%Y-%m-%dT%T")
#ENDDATE=$CURRENTDATE
ENDDATE=2023-05-06T23:59:59

CLOUDCOVER="[0,95]"

# Baseurl to reach the CDSE catalog with json output
BASEURL="http://catalogue.dataspace.copernicus.eu/resto/api/collections/Sentinel2/search.json?"

YEAR=${ENDDATE:0:4}

for TILE in ${TILES[@]}

do
    # Query the catalog with previously defined variables, 20 is the default max record number, which you can adapt to your needs
    # See https://documentation.dataspace.copernicus.eu/APIs/OpenSearch.html#output-sorting-and-limiting for further options for sorting
    QUERY="productType=S2MSI2A&startDate=${STARTDATE}.000Z&completionDate=${ENDDATE}.000Z&cloudCover=${CLOUDCOVER}&productIdentifier=${TILE}&maxRecords=20"
    # echo $BASEURL$QUERY
    wget --output-document=query_${YEAR}_${TILE}.json $BASEURL$QUERY

    # JSON includes much more information than only product paths -> extract product path from the JSON and safe to 
    jq -r  '.. | .productIdentifier? | select( . != null ) ' query_${YEAR}_${TILE}.json  | grep "/eodata/" > name_${YEAR}_${TILE}.txt

    # Read the file with product paths and download each file from CDSE to Allas bucket defined above
    while IFS="" read -r FILE || [ -n "$FILE" ]
    do
        echo $FILE
        # Rclone needs the filename in destination, otherwise the source .SAFE directory is unpacked without the .SAFE directory
        SAFENAME="$(basename -- $FILE)"
        rclone copy -P -v cdse:$FILE s3allas:$BUCKETBASENAME-${YEAR}-${TILE}/$SAFENAME
    done < name_${YEAR}_${TILE}.txt
done
