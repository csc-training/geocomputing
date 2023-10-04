#!/bin/bash

# Get the file name given as input (argument) for this script.
in=$1

# Define output file name, based on input file name
out=$(basename $in)

#Change the coordinate system to EPSG:2393, which is the old Finnish YKJ (=KKJ3)
gdalwarp $in $out -of COG -t_srs EPSG:2393
