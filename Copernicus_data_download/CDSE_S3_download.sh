#!/bin/bash

###############
# Example script to query and download data from Copernicus Data Space Ecosystem.
# See readme for connection set up details.
#
# Based on script provided by Maria Yli-Heikkilä (LUKE) - adapted to CDSE by Samantha Wittke and Kylli Ek, CSC - IT center for Science

# Provide Sentinel-2 tilenames that you want to download
TILES=("T34VDM" "T34VEM" "T34VEN")

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
        # Define folder name for each .SAFE file
        SAFENAME="$(basename -- $FILE)"
		
		# Download to local disk
		rclone copy -P -v cdse:$FILE /scratch/project_2000599/cdse/$SAFENAME
		
		# OR Download to Allas
        #rclone copy -P -v cdse:$FILE s3allas:yourBucketName/$SAFENAME
    done < name_${YEAR}_${TILE}.txt
done