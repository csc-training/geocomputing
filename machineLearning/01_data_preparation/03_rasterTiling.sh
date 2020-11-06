### TILING FOR CNN
# Satellite images are usually too big for CNN models as such, se we need to tile them to smaller pieces.
# In our example the original image is 3000 x 2800 pixels, and the model 512 x 512 pixels.
# For better augmentation we make the training tiles bigger (650 x 650) than the model, so that at training time a random clip can be done.
# Use also overlapping tiling scheme to get more training data.
# For prediction no overlap is used, because prediction tiles bigger than model seemed to cause unwanted side-effects.

# Load the module in Puhti that has gdal installed
module load geoconda

# Tile the satellite image for training with GDAL.
export DATA_DIR=/scratch/project_2002044/data/GIS_ML_COURSE_DATA/data/forest
mkdir tiles
mkdir tiles/image_training_tiles_650
gdal_retile.py -ps 650 650 -overlap 300 -targetDir tiles/image_training_tiles_650 $DATA_DIR/T34VFM_20180829T100019_clipped_scaled.tif
# -ps - tile size in pixels
# -overlap - overlap of tiles in pixels
# -targetDir - the directory of output tiles

# Tile the labels with the same setting as the image. Only spurce for CNN
mkdir tiles/label_tiles_650
gdal_retile.py -ps 650 650 -overlap 300 -targetDir tiles/label_tiles_650 $DATA_DIR/forest_spruce_clip.tif

# Labels for multiclass CNN
mkdir tiles/labels_all_classes_tiles_650

gdal_retile.py -ps 650 650 -overlap 300 -targetDir tiles/labels_all_classes_tiles_650 $DATA_DIR/forest_species_reclassified_clip.tif

# Tile the satellite image for predicting with the bigger bbox and model size tiles.
mkdir tiles/image_prediction_tiles_512
gdal_retile.py -ps 512 512 -targetDir tiles/image_prediction_tiles_512 $DATA_DIR/T34VFM_20180829T100019_scaled.tif

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
rm -f tiles/image_prediction_tiles_512/*_12_*.tif
rm -f tiles/image_prediction_tiles_512/*_15.tif

### COMPRESSING 
## Lastly let's compress the tiles .tar files. .tar files are very similar than .zip files
## This is done so that when we run the training job on Puhti, it can use the fast local disk rather than /scratch
cd tiles
tar -czvf spruce.tar image_training_tiles_650 label_tiles_650
tar -czvf forest.tar image_training_tiles_650 labels_all_classes_tiles_650
tar -czvf spruce_prediction.tar image_prediction_tiles_512
cd ..
