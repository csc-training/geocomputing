#!/bin/bash

# Change to the folder where you have the input files
cd /appl/data/geo/mml/dem10m/etrs-tm35fin-n2000/W3/W33

#Find the files that have .tif ending, we do not want to process the .tif.aux.xml files in the same folders.
for i in $(find . -name '*.tif')

#Process the files
do
    #Remove './' from the beginning of the find results. 
    i=`echo $i | sed "s/\.\///"`
	#Change the coordinate system to EPSG:2393, which is the old Finnish YKJ (=KKJ3)
    gdalwarp $i /scratch/project_2002044/trainingXX/gdal/$i -co compress=deflate -co tiled=yes -t_srs EPSG:2393
	# Add overviews
    gdaladdo --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC_OVERVIEW YCBCR --config INTERLEAVE_OVERVIEW PIXEL /scratch/project_2002044/trngXX/gdal/$i 4 16 64
done