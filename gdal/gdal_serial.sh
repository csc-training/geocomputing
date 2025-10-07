#!/bin/bash

# Find the files that have .tif ending, we do not want to process the .tif.aux.xml files in the same folders.
for i in $(find /appl/data/geo/mml/dem10m/2019/W3/W33 -name '*.tif')

# Process the files
do
    # Define output file name, based on input file name
	out=$(basename $i)
	# Change the coordinate system to EPSG:2393, which is the old Finnish YKJ (=KKJ3)
	# ToDo: change project name and username in the row below
    gdalwarp $i /scratch/project_2015299/students/$USER/geocomputing/gdal/$out -of COG -t_srs EPSG:2393
done
