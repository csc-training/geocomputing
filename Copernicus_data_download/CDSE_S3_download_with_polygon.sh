#!/bin/bash

###############
# Example script to query and download data from Copernicus Data Space Ecosystem WITH POLYGON.
# See readme for connection set up details.
#
# Based on script provided by Maria Yli-Heikkilä (LUKE) - adapted to CDSE by Samantha Wittke and Kylli Ek, CSC - IT center for Science


# If you suitable polygon ready, then save it as CSV with geometry in WKT
# https://geojson.io/ can be used for quick creation of the input file in GeoJson format - draw a polygon on map and save the text to a .json file.
# The input file could be also .shp, .gpkg or some other format supported by GDAL.
ogr2ogr -f CSV area.csv input.json -lco GEOMETRY=AS_WKT

# Alternatively, if you do not have the polygon ready, but would like to calculate based on some exsisting vector file:
# Note that besides changing the name of the file, you have to change also the layer name, in case of Shape file, it is the same as file name.
#
# ogr2ogr -f CSV area.csv /appl/data/geo/tilastokeskus/tieliikenne/2022/tieliikenne_2022.shp -dialect SQLite -sql "select st_concavehull(st_collect(geometry)) from tieliikenne_2022" -lco GEOMETRY=AS_WKT -t_srs EPSG:4326

# Get the WKT polygon from file and remove quotes.
# Only the first polygon of the the file is used.
wkt=$(sed '2q;d' area.csv)
wkt2=${wkt//\"/}

# Provide the timedelta - start date and time
STARTDATE=2023-05-01T00:00:00

# end date and time ; fixed or set to current date
#CURRENTDATE=$(date +"%Y-%m-%dT%T")
#ENDDATE=$CURRENTDATE
ENDDATE=2023-05-06T23:59:59

CLOUDCOVER="[0,95]"

# Baseurl to reach the CDSE catalog with json output
BASEURL="http://catalogue.dataspace.copernicus.eu/resto/api/collections/Sentinel2/search.json?"

# Query the catalog with previously defined variables, 20 is the default max record number, which you can adapt to your needs
# See https://documentation.dataspace.copernicus.eu/APIs/OpenSearch.html#output-sorting-and-limiting for further options for sorting
QUERY="productType=S2MSI2A&startDate=${STARTDATE}.000Z&completionDate=${ENDDATE}.000Z&cloudCover=${CLOUDCOVER}&geometry=${wkt2}&maxRecords=1"
# echo $BASEURL$QUERY

wget --output-document=query.json "$BASEURL$QUERY"

# JSON includes much more information than only product paths -> extract product path from the JSON and safe to 
jq -r  '.. | .productIdentifier? | select( . != null ) ' query.json  | grep "/eodata/" > safe_files.txt

# Read the file with product paths and download each file from CDSE
while IFS="" read -r FILE || [ -n "$FILE" ]
do
	echo $FILE
	# Define folder name for each .SAFE file
	SAFENAME="$(basename -- $FILE)"
	
	# Download to local disk
	rclone copy -P -v cdse:$FILE /scratch/project_2000599/cdse/$SAFENAME
	
	# OR Download to Allas
	#rclone copy -P -v cdse:$FILE s3allas:yourBucketName/$SAFENAME
done < safe_files.txt

# Delete temporary files
rm area.csv
rm query.json
rm safe_files.txt