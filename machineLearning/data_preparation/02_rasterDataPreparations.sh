#!/bin/bash
# In this exercise we prepare data for classification based on a raster satellite image and vector polygon.
# The aim is to train a model that would recognize different species of forest from the satellite image.
# The exercise data is:
# * Forest stands from Forest center (Metsäkeskus). https://www.metsaan.fi/paikkatietoaineistot
# * Sentinel 2A satellite image from ESA. https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-2/data-products


# GET DATA
cd classification
wget https://aineistot.metsaan.fi/avoinmetsatieto/Metsavarakuviot/Maakunta/MV_Uusimaa.zip
wget https://aineistot.metsaan.fi/avoinmetsatieto/Metsavarakuviot/Kunta/MV_Salo.zip
# Download the Sentinel image from https://scihub.copernicus.eu/, S2B_MSIL2A_20180829T100019_N0208_R122_T34VFM_20180829T184909
# Scihub requires registration, but the files are available for free.

# Unzip the forest stands datasets
unzip MV_Uusimaa.zip
unzip MV_Salo.zip

### SENTINEL SATELLITE IMAGE PREPARATIONS
# Select bands 08, 04 and 03 for exercise and clip them to two areas, one for training, and one for predicting.
# The training area is smaller, because in Lohja community the forest data seems to be missing a lot of forest polygons, so we want to exclude that.

# Go to the folder of original Sentinel data
cd ..\S2B_MSIL2A_20180829T100019_N0208_R122_T34VFM_20180829T184909.SAFE\GRANULE\L2A_T34VFM_A007727_20180829T100017\IMG_DATA\R10m

# Select the bands used: 08 (NIR), 04 and 03 and make a virtual raster file of them
gdalbuildvrt -separate T34VFM_20180829T100019.vrt T34VFM_20180829T100019_B08_10m.jp2 T34VFM_20180829T100019_B04_10m.jp2 T34VFM_20180829T100019_B03_10m.jp2
# -separate, use the input files as bands, and not as mapsheets

# Normalize the pixel values from 0 to 10 000 -> 0 to 1. This is specific to Sentinal 2A product, that it has to be devided with 10 0000.
# Clip to exercise area.
gdal_translate -projwin 614500 6668500 644500 6640500 T34VFM_20180829T100019.vrt ..\..\..\..\..\classification\T34VFM_20180829T100019_clipped_scaled.tif -ot Float32 -scale 0 10000 0 1
gdal_translate -projwin 604500 6698500 677000 6640000 T34VFM_20180829T100019.vrt ..\..\..\..\..\classification\T34VFM_20180829T100019_scaled.tif -ot Float32 -scale 0 10000 0 1

# Go back to exercise folder
cd ..\..\..\..\..\classification

### FOREST STANDS PREPARATIONS
# Clip to study area and merge the two GeoPackage files. Exclude polygons, that have no main tree species value.
ogr2ogr -f GPKG -t_srs epsg:32634 -spat 614500 6640500 644500 6668500 -spat_srs epsg:32634 -where "maintreespecies>0" forest_clipped.gpkg MV_Salo.gpkg stand
ogr2ogr -f GPKG -t_srs epsg:32634 -spat 614500 6640500 644500 6668500 -spat_srs epsg:32634 -where "maintreespecies>0" -append -update forest_clipped.gpkg MV_Uusimaa.gpkg stand
# -t_srs new coordinate system, epsg:3067 is the code for ETRS-TM35FIN
# -spat bbox of study area in UTM 34N coordinates
# -spat_srs EPSG code of the spat coodrinates - UTM 34N
# -where, select only polygons that have the maintreespecies value. In the dataset were some polygons with -1 value.

# Rasterize forest stand polygons.
# It is critical to use same cell size and bbox as the satellite image. If not know, you can check with: 
# gdalinfo T34VFM_20180829T100019_clipped_scaled.tif
# Note! gdal_translate and gdal_rasterize have different order of ymin and ymax coordinates.
gdal_rasterize -a maintreespecies -ot Byte -tr 10 10 -te 614500 6640500 644500 6668500 forest_clipped.gpkg -l stand forest_species.tif
# -a - the attribute column where tree species are given
# -ot - numeric format of cell, Byte=integer, max 255
# -tr - raster cell size in coordinate system units, in this case meters.
# -te - bbox of output raster
# -l - layer/table of the input GeoPackage

# Some tree species have very little areas in the study are, so there are very few pixels for these classes.
# These are mostly different deciduous trees (class >= 3), so we combine them to one deciduous tree classes (class=3).
# As we result we have 3 classes of forest and one class for no forest:
# 1 - pine
# 2 - spruce
# 3 - deciduous trees
# 0 - no forest
gdal_calc -A forest_species.tif --outfile=forest_species_reclassified.tif --calc="3*(A>=3)+1*(A==1)+2*(A==2)" --NoDataValue=0
# -A input file
# --calc, how to recalculate the values, we keep values aof 1 and 1 as they are. And assign 3 to everything that was 3 or bigger.

# For CNN we will use only spruce forest
gdal_rasterize -a maintreespecies -tr 10 10 -ot Byte -te 614500 6640500 644500 6668500 -where "maintreespecies=2" forest_clipped.gpkg -l stand forest_spruce.tif
# Otherwise same as above, but selecting only spruce forest (maintreespecies=2) with -where

# Rescale the image from 0 to 2 -> 0 to 1.
gdal_translate forest_spruce.tif forest_spruce_scaled.tif -ot Byte -scale 0 2 0 1

### TILING FOR CNN
# Satellite images are usually too big for CNN models as such, se we need to tile them to smaller pieces.
# In our example the original image is 3000 x 2800 pixels, and the model 512 x 512 pixels.
# For better augmentation we make the training tiles bigger (650 x 650) than the model, so that at training time a random clip can be done.
# Use also overlapping tiling scheme to get more training data.
# For prediction no overlap is used, because prediction tiles bigger than model seemed to cause unwanted side-effects.

# Tile the satellite image for training with GDAL.
mkdir imageTiles650
gdal_retile -ps 650 650 -overlap 300 -targetDir imageTiles650 T34VFM_20180829T100019_clipped_scaled.tif
# -ps - tile size in pixels
# -overlap - overlap of tiles in pixels
# -targetDir - the directory of output tiles

# Tile the labels with the same setting as the image.
mkdir labels650
gdal_retile -ps 650 650 -overlap 300 -targetDir labels650 forest_spruce_scaled.tif

# Tile the satellite image for predicting with the bigger bbox.
mkdir imageTiles512
gdal_retile -ps 512 512 -targetDir imageTiles512 T34VFM_20180829T100019_scaled.tif

# CNN model requires at least 512x512 size of images, so the remove the files from right and bottom edge, that are too small.
# Please note that the last column and row of tiles may be smaller than requested.
# In our case for training data, only the last row of tiles is too low, so we delete these files.
cd imageTiles650
del *_8_*.tif

cd ..\labels650
del *_8_*.tif

# For predicting data we have to remove last column and row of tiles.
cd ..\imageTiles512
del *_12_*.tif
del *_15.tif

# Solaris wants to get the tile paths as a CSV file.
# See: https://solaris.readthedocs.io/en/latest/tutorials/notebooks/creating_im_reference_csvs.html
python make_csv.py
