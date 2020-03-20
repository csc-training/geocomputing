#!/bin/bash
# In this exercise we prepare data for the other excercises
# The raw data to be prepared is:
#   * Forest stands from Forest center (Metsäkeskus). https://www.metsaan.fi/paikkatietoaineistot
#   * Sentinel 2A satellite image (10m x 10m) from ESA. https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-2/data-products
#   * a False color aerial image (0.5m x 0.5m) from the NLS https://www.maanmittauslaitos.fi/kartat-ja-paikkatieto/asiantuntevalle-kayttajalle/tuotekuvaukset/ilmakuva
#   * Building footprints from the Topographic Database (NLS) https://www.maanmittauslaitos.fi/kartat-ja-paikkatieto/asiantuntevalle-kayttajalle/tuotekuvaukset/maastotietokanta-0
#       * Buildings have been separated from the data with the following command
#         ogr2ogr -f "GPKG" -spat 422000 6768000 428000 6762000 buildings_M4311G.gpkg /appl/data/geo/mml/maastotietokanta/2019/gpkg/MTK-rakennus_19-01-23.gpkg -sql "SELECT * FROM rakennus"

# *** NOTE! WINDOWS USERS CHANGE THESE IN THIS SCRIPT ***
# - replace / with \
#	- replace command rm with del
#	- replace gdal_retile.py, gdal_calc.py with gdal_retile and gdal_calc

### DOWNLOAD DATA FROM ALLAS
cd classification
wget <ALLAS-ZIP-WITH-ALL-RAW-DATA> #TODO
unzip ALLAS_ZIP.zip

### SENTINEL SATELLITE IMAGE PREPARATIONS
# Select bands 08, 04 and 03 for exercise and clip them to three areas, one for training, and one for predicting.
# The training area is smaller, because in Lohja community the forest data seems to be missing a lot of forest polygons, so we want to exclude that.

# Go to the folder of original Sentinel data
cd S2B_MSIL2A_20180829T100019_N0208_R122_T34VFM_20180829T184909.SAFE/GRANULE/L2A_T34VFM_A007727_20180829T100017/IMG_DATA/R10m

# Select the bands used: 08 (NIR), 04 (RED) and 03 (GREEN) and make a virtual raster file of them
gdalbuildvrt -separate T34VFM_20180829T100019.vrt T34VFM_20180829T100019_B08_10m.jp2 T34VFM_20180829T100019_B04_10m.jp2 T34VFM_20180829T100019_B03_10m.jp2
# -separate, use the input files as bands, and not as mapsheets

# Scale the pixel values from 0 to 10 000 -> 0 to 1. In Sentinel images, the original values have been multiplied by 10 000 to get rid of decimals (0.0001 takes more disk space than 10 000)
# Clip the training area
gdal_translate -projwin 614500 6668500 644500 6640500 T34VFM_20180829T100019.vrt ../../../../../T34VFM_20180829T100019_clipped_scaled.tif -ot Float32 -scale 0 10000 0 1
# Clip the original image also a bit smaller for predictions
gdal_translate -projwin 604500 6698500 677000 6640000 T34VFM_20180829T100019.vrt ../../../../../T34VFM_20180829T100019_scaled.tif -ot Float32 -scale 0 10000 0 1

# Go back to the "forest" data folder
cd ../../../../../

### FOREST STANDS PREPARATIONS

# Merge the two GeoPackage files to file called forest_clipped.gpkg. Exclude polygons, that have no main tree species value.
ogr2ogr -f GPKG -t_srs epsg:32634-spat_srs epsg:32634 -where "maintreespecies>0" forest_clipped.gpkg MV_Salo.gpkg stand
ogr2ogr -f GPKG -t_srs epsg:32634 -spat_srs epsg:32634 -where "maintreespecies>0" -append -update forest_clipped.gpkg MV_Uusimaa.gpkg stand

# Parameter explanation
#     -t_srs new coordinate system, epsg:3067 is the code for ETRS-TM35FIN
#     -spat bbox of study area in UTM 34N coordinates
#     -spat_srs EPSG code of the spat coodrinates - UTM 34N
#     -where, select only polygons that have the maintreespecies value. In the dataset were some polygons with -1 value.

# Rasterize forest stand polygons and clip to the same extent as the full Sentinel image
gdal_rasterize -a maintreespecies -ot Byte -tr 10 10 -te 604500 6640000 677000 6698500 forest_clipped.gpkg -l stand forest_species.tif

# Classify the forest main tree species to three classes: Pine (1), Spruce (2), Deciduous trees (3), No trees (0)
gdal_calc.py -A forest_species.tif --outfile=forest_species_reclassified.tif --calc="3*(A>=3)+1*(A==1)+2*(A==2)" --NoDataValue=0

# Some excercises use only the spruce data. Rasterize it from the original gpkg file and scale it from 0 2 to 0 1
gdal_rasterize -a maintreespecies -ot Byte -tr 10 10 -te 604500 6640000 677000 6698500 -where "maintreespecies=2" forest_clipped.gpkg -l stand forest_spruce02.tif
gdal_translate forest_spruce02.tif -ot Byte -scale 0 2 0 1 forest_spruce.tif

# Clip training area for both 3-class and just 1-class datasets and for spruce change the value of spruce from 2 to 1
gdal_translate forest_spruce.tif forest_spruce_clip.tif -ot Byte -projwin 614500 6668500 644500 6640500
gdal_translate forest_species_reclassified.tif forest_species_reclassified_clip.tif -ot Byte -projwin 614500 6668500 644500 6640500

### AERIAL IMAGE PREPARATIONS
# Clip the aerial image for speeding up the training times of our models
gdal_translate -projwin 422000 6765000 425000 6762000 M4311G.jp2 M4311G_clip.tif

### BUILDING FOOTPRINTS PREPARATIONS
# Rasterize the building footprint polygons to a raster and clip it to the same extent as the aerial image
gdal_rasterize buildings_M4311G.gpkg -ot Byte -te 422000 6762000 425000 6765000 -tr 0.5 0.5 -burn 1 -l SELECT building_footprints_clip.tif

# These were temporary outputs. You can delete it after the previous steps
rm forest_species.tif
rm forest_spruce02.tif

### TILING FOR CNN
# Satellite images are usually too big for CNN models as such, se we need to tile them to smaller pieces.
# In our example the original image is 3000 x 2800 pixels, and the model 512 x 512 pixels.
# For better augmentation we make the training tiles bigger (650 x 650) than the model, so that at training time a random clip can be done.
# Use also overlapping tiling scheme to get more training data.
# For prediction no overlap is used, because prediction tiles bigger than model seemed to cause unwanted side-effects.

# Tile the satellite image for training with GDAL.
mkdir tiles
mkdir tiles/image_training_tiles_650
gdal_retile.py -ps 650 650 -overlap 300 -targetDir tiles/image_training_tiles_650 T34VFM_20180829T100019_clipped_scaled.tif
# -ps - tile size in pixels
# -overlap - overlap of tiles in pixels
# -targetDir - the directory of output tiles

# Tile the labels with the same setting as the image. Only spurce for CNN
mkdir tiles/label_tiles_650
gdal_retile.py -ps 650 650 -overlap 300 -targetDir tiles/label_tiles_650 forest_spruce_clip.tif

# Labels for multiclass CNN
mkdir tiles/labels_all_classes_tiles_650

gdal_retile.py -ps 650 650 -overlap 300 -targetDir tiles/labels_all_classes_tiles_650 forest_species_reclassified_clip.tif

# Tile the satellite image for predicting with the bigger bbox and model size tiles.
mkdir tiles/image_prediction_tiles_512
gdal_retile.py -ps 512 512 -targetDir tiles/image_prediction_tiles_512 T34VFM_20180829T100019_scaled.tif

# CNN model requires at least 512x512 size of images, so the remove the files from right and bottom edge, that are too small.
# Sentinel tiles
rm -f tiles/image_training_tiles_650/*_8_*.tif
rm -f tiles/image_training_tiles_650/*_8.tif

# Spruce label tiles
rm -f tiles/label_tiles_650/*_8_*.tif
rm -f tiles/label_tiles_650/*_8.tif

# Multiclass label tiles
rm -f tiles/labels_all_classes_tiles_650/*_8_*.tif
rm -f tiles/labels_all_classes_tiles_650/*_8.tif

# For predicting data we have to remove last column and row of tiles.
cd tiles/image_prediction_tiles_512/
rm -f tiles/image_prediction_tiles_512/*_12_*.tif
rm -f tiles/image_prediction_tiles_512/*_15.tif
cd ..

### COMPRESSING 
## Lastly let's compress the tiles-folder to single .tar file. .tar files are very similar than .zip files
tar -czvf spruce.tar image_training_tiles_650 label_tiles_650
tar -czvf forest.tar image_training_tiles_650 labels_all_classes_tiles_650

