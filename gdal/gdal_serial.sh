#!/bin/bash

#Find the files that have .tif ending, we do not want to process the .tif.aux.xml files in the same folders.
for i in $(find /appl/data/geo/mml/dem10m/2019/V5/V53 -name '*.tif')

#Process the files
do
    # Define output file name, based on input file name
	out=$(basename $i)
	#Change the coordinate system to EPSG:2393, which is the old Finnish YKJ (=KKJ3)
	# ToDo: change project name and username in the row below
    gdalwarp $i /scratch/project_200xxxx/students/cscusername/geocomputing/gdal/$i -co compress=deflate -co tiled=yes -t_srs EPSG:2393
	# Add overviews
	# ToDo: change project name and username in the row below
    gdaladdo --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC_OVERVIEW YCBCR --config \
	INTERLEAVE_OVERVIEW PIXEL /scratch/project_200xxxx/students/cscusername/geocomputing/gdal/$i 4 16 64
done
