# Change coordinate system of many files with GDAL and bash script.

**GDAL** provides many useful tools. In this example, we will reproject the coordinate system of multiple files in a folder, and add overviews to the same files. 
We do not use R nor Python, but GDAL commands from a simple Linux bash script.

* Start an [interactive session](https://docs.csc.fi/computing/running/interactive-usage/)
```
sinteractive -i
```
* Open the [gdal.sh](gdal.sh) file with nano in Puhti and fix the path of output file and save the file.
* Load [GDAL module](https://docs.csc.fi/apps/gdal/)
```
module load gcc/9.1.0 gdal
```
* Check the original file with gdalinfo. What is the coordinate system? Are the files tiled? Do they have overviews?
```
gdalinfo /appl/data/geo/mml/dem10m/etrs-tm35fin-n2000/W3/W33/W3333.tif
```
* Change the permissions of gdal.sh, so that it can be executed: 
```
chmod 770 gdal.sh
```
* Run the script: 
```
./gdal.sh
```
* Check the result file with `gdalinfo`. What is the coordinate system? Are the files tiled? Do they have overviews?
