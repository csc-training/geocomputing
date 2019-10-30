import solaris as sol
import torch
import rasterio
import rasterio.merge
import pandas as pd
import time
import os
from PredictSpruceForestsModel import PredictSpruceForestsModel


### FILL HERE the path where your data is. e.g "/scratch/project_2000599/students/26/data"
base_folder = ""

tile_output_folder = os.path.join(base_folder,"tiles")

### The whole image (prediction), training image (clipped from the whole img) and the label image
training_image_path = os.path.join(base_folder,"T34VFM_20180829T100019_training_clip.tif")
training_label_path = os.path.join(base_folder,"forest_spruce.tif")
prediction_image_path = os.path.join(base_folder,"T34VFM_20180829T100019.tif")

training_image_tile_subfolder = os.path.join(tile_output_folder,"image_tiles")
training_label_tile_subfolder = os.path.join(tile_output_folder, "label_tiles")
prediction_image_tile_subfolder = os.path.join(tile_output_folder,"prediction_tiles")

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

def checkGPUavailability():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if device.type == 'cuda':
        print("We have a GPU available! The model is: ",torch.cuda.get_device_name(0))
    else:
        print("Sadly no GPU available. :( you have settle with a CPU. Good luck!")

def createTileListFiles():
    #### Create lists of the tile filenames
    list_of_training_tiles = os.listdir(training_image_tile_subfolder)
    list_of_label_tiles = os.listdir(training_label_tile_subfolder)
    list_of_prediction_tiles = os.listdir(prediction_image_tile_subfolder)

    ### Add the whole path to the filenames
    list_of_training_tiles = [os.path.join(training_image_tile_subfolder, i) for i in list_of_training_tiles]
    list_of_label_tiles = [os.path.join(training_label_tile_subfolder, i) for i in list_of_label_tiles]
    list_of_prediction_tiles = [os.path.join(prediction_image_tile_subfolder, i) for i in list_of_prediction_tiles]

    ### Sort the two lists used in training so they match
    list_of_training_tiles.sort()
    list_of_label_tiles.sort()

    ### Create a pandas dataframe that has the training image filepath and label image filepath as columns and write it to csv
    training_filename_df = pd.DataFrame({'image': list_of_training_tiles, 'label': list_of_label_tiles})
    print(training_filename_df.head())
    training_filename_df.to_csv(os.path.join(base_folder, 'tile_filepaths_for_training.csv'), encoding='utf-8')

    ### Create a pandas dataframe that has the prediction image filepaths as a column and write it to csv
    prediction_filename_df = pd.DataFrame({'image': list_of_prediction_tiles})
    prediction_filename_df.to_csv(os.path.join(base_folder, 'tile_filepaths_for_prediction.csv'), encoding='utf-8')

def trainModel(config,custom_model_dict):
    ### This function trains the convolutional neural network model

    start_time = time.time()
    print('Training the model...')
    trainer = sol.nets.train.Trainer(config, custom_model_dict=custom_model_dict)
    trainer.train()
    end_time = time.time()

    print('training took {} seconds'.format(end_time - start_time))

def predictForTiles(config,custom_model_dict):
    ### This function runs the prediction for another dataset using the trained model
    print('config loaded. Initializing model...')
    xdxd_inferer = sol.nets.infer.Inferer(config, custom_model_dict=custom_model_dict)
    print('model initialized. Loading dataset...')
    inf_df = sol.nets.infer.get_infer_df(config)
    print('dataset loaded. Running inference on the image.')
    start_time = time.time()
    print(inf_df.head())
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
    print(list_of_rasters)
    mosaic, out_trans = rasterio.merge.merge(list_of_rasters)
    print(mosaic.shape)
    out_metafile = raster.meta.copy()

    out_metafile.update({"driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": out_trans,
            "crs": "+proj=utm +zone=34 +datum=WGS84 +units=m +no_defs "
        }
    )
    print(out_metafile)

    output_path = os.path.join(base_folder,"predicted_spruce.tif")
    with rasterio.open(output_path, "w", **out_metafile) as dest:
        dest.write(mosaic)



def main():
    ### Let's check if we have a valid GPU at use
    checkGPUavailability()

    ### Let's split the input images to tiles that the CNN can use
    createTileListFiles()

    ### Let's load the configuration .yml file for the prediction phase
    training_config = sol.utils.config.parse(os.path.join(base_folder,'scripts','config_training.yml'))
    custom_model_dict = {'model_name': 'PredictSpruceForestsModel', 'weight_path': None, 'weight_url': None,
                         'arch': PredictSpruceForestsModel}


    trainModel(training_config,custom_model_dict)


    ### Let's load the configuration .yml file for the prediction phase
    prediction_config = sol.utils.config.parse(os.path.join(base_folder, 'scripts', 'config_prediction.yml'))
    custom_model_dict = {'model_name': 'PredictSpruceForestsModel',
                         'weight_path': prediction_config['training']['model_dest_path'],
                         'weight_url': None,
                         'arch': PredictSpruceForestsModel}

    predictForTiles(prediction_config,custom_model_dict)

    ### The prediction is done to single tiles, this function merges them back to a larger image
    mergeOutputTiles(prediction_config['inference']['output_dir'])

if __name__ == '__main__':
    ### This part just runs the main method and times it
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(round(((end - start) / 60), 3)) + " minutes")
