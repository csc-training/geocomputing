import solaris as sol
import torch
import rasterio
import rasterio.merge
import rasterio.mask
import pandas as pd
import time
import os
from PredictSpruceForestsModel import PredictSpruceForestsModel
import sys

### The first (and only) input argument for this script is the folder where data exists
if len(sys.argv) != 2:
   print('Please give the data directory')
   sys.exit()

base_folder=sys.argv[1]

### This is the folder of this file. We use it to fetch the .yml files
script_folder = os.path.dirname(os.path.realpath(__file__))

### Rest of the hierarchical subfolder structure
tile_output_folder = os.path.join(base_folder,"tiles")
prediction_image_tile_subfolder = os.path.join(tile_output_folder,"image_prediction_tiles_512")

### Output path for the predicted image 
predicted_image_output_path = os.path.join(base_folder,"spruce_prediction_1200_epochs.tif")

### Validation image which will be compared to the predicted one
test_image_path = os.path.join(base_folder,"validation","forest_spruce_scaled_validation_2.tif")

def checkGPUavailability():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if device.type == 'cuda':
        print("We have a GPU available! The model is: ",torch.cuda.get_device_name(0))
    else:
        print("Sadly no GPU available. :( you have settle with a CPU. Good luck!")

def createTileListFiles():
    #### Create lists of the tile filenames
    list_of_prediction_tiles = os.listdir(prediction_image_tile_subfolder)

    ### Add the whole path to the filenames
    list_of_prediction_tiles = [os.path.join(prediction_image_tile_subfolder, i) for i in list_of_prediction_tiles]

    ### Create a pandas dataframe that has the prediction image filepaths as a column and write it to csv
    prediction_filename_df = pd.DataFrame({'image': list_of_prediction_tiles})
    prediction_filename_df.to_csv(os.path.join(script_folder, 'tile_filepaths_for_prediction.csv'), encoding='utf-8')

def predictForTiles(config,custom_model_dict):
    ### This function runs the prediction for another dataset using the trained model
    print('config loaded. Initializing model...')
    xdxd_inferer = sol.nets.infer.Inferer(config, custom_model_dict=custom_model_dict)
    print('model initialized. Loading dataset...')
    inf_df = sol.nets.infer.get_infer_df(config)
    print('dataset loaded. Running inference on the image.')
    start_time = time.time()
    xdxd_inferer(inf_df)
    end_time = time.time()
    print('running inference on one image took {} seconds'.format(end_time - start_time))

def mergeOutputTiles(predicted_tiles_folder):
    ### This function loops over the predicted tiles, adds the Coordinate system information to the tiles and finally merges all tiles

    ### Empty list to be populated with rasterio objects from tiles
    list_of_rasters = []

    ### This loops all files in the predicted tiles folder and changes the crs to match the reference tile crs, also adds tiles to a list for merging
    for filename in os.listdir(predicted_tiles_folder):
        if filename.endswith(".tif"):
            full_filepath = os.path.join(predicted_tiles_folder, filename)
            reference_tile = rasterio.open(os.path.join(prediction_image_tile_subfolder, filename))
            with rasterio.open(full_filepath, 'r+') as raster:
                raster.crs = reference_tile.crs
                raster.transform = reference_tile.transform

            raster = rasterio.open(full_filepath)
            list_of_rasters.append(raster)

    print("Succesfully added CRS information to the predicted tiles")
    mosaic, out_trans = rasterio.merge.merge(list_of_rasters)
    out_metafile = raster.meta.copy()

    out_metafile.update({"driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": out_trans,
            "crs": "+proj=utm +zone=34 +datum=WGS84 +units=m +no_defs "
        }
    )

    with rasterio.open(predicted_image_output_path, "w", **out_metafile) as dest:
        dest.write(mosaic)

def estimateModel():
    
    # Open image files of predicted data and test data
    with rasterio.open(predicted_image_output_path, 'r') as prediction_dataset:      
        with rasterio.open(test_image_path, 'r') as test_labels_dataset:           
            
            #Find out the overlappin area of two images.
            #Because of tiling the prediction image is slightly smaller than the original clip.
            left = max(prediction_dataset.bounds.left,test_labels_dataset.bounds.left)
            bottom = max(prediction_dataset.bounds.bottom,test_labels_dataset.bounds.bottom)
            right = min(prediction_dataset.bounds.right,test_labels_dataset.bounds.right)
            top = min(prediction_dataset.bounds.top,test_labels_dataset.bounds.top)
            
            common_bbox = {
                        "type": "Polygon",
                        "coordinates": [[
                            [left, bottom],
                            [left, top],
                            [right, top],
                            [right, bottom],
                            [left, bottom]]]}
                        
            # Read data from only the overlapping area
            y_pred, transform = rasterio.mask.mask(prediction_dataset, common_bbox, crop=True)
            y_true, transform = rasterio.mask.mask(test_labels_dataset, common_bbox, crop=True)

            ### Let's print the shapes of both images. They need to be the same
            print("Shape of the Prediction image clip: ",  y_pred.shape)
            print("Shape of the Validation image clip: ",  y_true.shape)

            ### Calculate the f1, precision and recall with Solaris
            ### prop_threshold determines what value is the dividing number on the predicted image. Below that will get 0, over it 1 so change it to your liking
            f1, precision, recall = sol.eval.pixel.f1(y_true,y_pred,prop_threshold=0.001,verbose=True)
            print("F1 score: {}, Precision: {}, Recall: {}".format(f1,precision,recall))


def main():
    ### Let's check if we have a valid GPU at use
    checkGPUavailability()

    ### Let's split the input images to tiles that the CNN can use
    createTileListFiles()

    ### Let's load the configuration .yml file for the prediction phase
    prediction_config = sol.utils.config.parse(os.path.join(script_folder, 'config_prediction.yml'))
    custom_model_dict = {'model_name': 'PredictSpruceForestsModel',
                        'weight_path': prediction_config['model_path'],
                        'weight_url': None,
                        'arch': PredictSpruceForestsModel}

    predictForTiles(prediction_config,custom_model_dict)

    ### The prediction is done to single tiles, this function merges them back to a larger image
    mergeOutputTiles(prediction_config['inference']['output_dir'])

    ### Evaluate the prediction with a validation image
    estimateModel()

if __name__ == '__main__':
    ### This part just runs the main method and times it
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(round(((end - start) / 60), 3)) + " minutes")
