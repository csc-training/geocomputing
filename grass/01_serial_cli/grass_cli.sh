#!/bin/sh
set -e

#Set file paths and names
DEMFILE="/appl/data/geo/mml/dem10m/2019/V4/V41/V4132.tif"
GRASSINPUT="V4132"
GRASSOUTPUT="contours"
OUTPUT="/scratch/project_2000599/grass/output/V4132.gpkg"

# Register external GeoTIFF in current mapset:
r.external input=$DEMFILE output=$GRASSINPUT --verbose --overwrite

# Set GRASS region
g.region raster=$GRASSINPUT

# Perform GRASS analysis, here calculate contours from DEM
r.contour in=$GRASSINPUT out=$GRASSOUTPUT minlevel=200 maxlevel=800 step=10 --overwrite

#Write output to file
v.out.ogr input=$GRASSOUTPUT output=$OUTPUT --overwrite

# These can be left out, just debug info
echo "\n\n ***DEBUG INFO***"
echo "GRASS version"
g.version

echo "GRASS env settings: gisdatabase, location, mapset"
g.gisenv

echo "Available datasets:"
g.list type=all -m

echo "Input file info"
r.info $GRASSINPUT --verbose

echo "Output  info"
v.info $GRASSOUTPUT --verbose