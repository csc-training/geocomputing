#!/bin/bash

###############
# Example script to 
# 1. Query Copernicus Data Space Ecosystem Sentinel-2 catalog based on startdate, enddate, cloudcover and tilename 
# 2. Download the found data from CDSE object storage to Allas object storage
#
# Requirements: Rclone setup to work with allas as [s3allas] (s3 setup connected to CSC project for Allas) and CDSE as [cdse].
# See [CSC EO guide](https://docs.csc.fi/support/tutorials/gis/eo_guide/) about how to set it up. 
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
    # Query the catalog with previously defined variables
    QUERY="productType=S2MSI2A&startDate=${STARTDATE}.000Z&completionDate=${ENDDATE}.000Z&cloudCover=${CLOUDCOVER}&productIdentifier=${TILE}"
    # echo $BASEURL$QUERY
    wget --output-document=query_$YEAR_$TILE.json $BASEURL$QUERY

    # JSON includes much more information than only product paths -> extract product path from the JSON
    jq -r  '.. | .productIdentifier? | select( . != null ) ' query_$YEAR_$TILE.json  | grep "/eodata/" > name_$TILE.txt

    # Read the file with product paths and download each file from CDSE to Allas bucket defined above
    while IFS="" read -r FILE || [ -n "$FILE" ]
    do
        echo $FILE
        # Rclone needs the filename in destination, otherwise the source .SAFE directory is unpacked without the .SAFE directory
        SAFENAME="$(basename -- $FILE)"
        rclone copy -P -v cdse:$FILE s3allas:$BUCKETBASENAME-$YEAR-$TILE/$SAFENAME
    done < name_$DATE_$TILE.txt
done
