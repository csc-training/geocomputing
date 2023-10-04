#!/bin/bash

# Get the file name given as input (argument) for this script.
in=$1

# Define output file name, based on input file name
out=$(basename $in)

#Change the coordinate system to EPSG:2393, which is the old Finnish YKJ (=KKJ3)
gdalwarp $in $out -co compress=deflate -co tiled=yes -t_srs EPSG:2393
# Add overviews
gdaladdo --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC_OVERVIEW YCBCR \
--config INTERLEAVE_OVERVIEW PIXEL $out 4 16 64
