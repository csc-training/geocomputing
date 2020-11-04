import solaris as sol
import torch
import rasterio
import rasterio.merge
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

### Folder where our training, label, prediction and result tiles will be
tile_output_folder = os.path.join(base_folder)

### This script's training and label tile folders
training_image_tile_subfolder = os.path.join(tile_output_folder,"image_training_tiles_650")
training_label_tile_subfolder = os.path.join(tile_output_folder, "label_tiles_650")

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

    ### Add the whole path to the filenames
    list_of_training_tiles = [os.path.join(training_image_tile_subfolder, i) for i in list_of_training_tiles]
    list_of_label_tiles = [os.path.join(training_label_tile_subfolder, i) for i in list_of_label_tiles]

    ### Sort the two lists used in training so they match
    list_of_training_tiles.sort()
    list_of_label_tiles.sort()

    ### Create a pandas dataframe that has the training image filepath and label image filepath as columns and write it to csv
    training_filename_df = pd.DataFrame({'image': list_of_training_tiles, 'label': list_of_label_tiles})
    training_filename_df.to_csv(os.path.join(script_folder, 'tile_filepaths_for_training.csv'), encoding='utf-8')

def trainModel(config,custom_model_dict):
    ### This function trains the convolutional neural network model

    start_time = time.time()
    print('Training the model...')
    trainer = sol.nets.train.Trainer(config, custom_model_dict=custom_model_dict)
    trainer.train()
    end_time = time.time()

    print('training took {} seconds'.format(end_time - start_time))


def main():
    ### Let's check if we have a valid GPU at use
    checkGPUavailability()

    ### Let's split the input images to tiles that the CNN can use
    createTileListFiles()

    ### Let's load the configuration .yml file for the prediction phase
    training_config = sol.utils.config.parse(os.path.join(script_folder,'config_training.yml'))
    custom_model_dict = {'model_name': 'PredictSpruceForestsModel', 'weight_path': None, 'weight_url': None,
                         'arch': PredictSpruceForestsModel}


    trainModel(training_config,custom_model_dict)


if __name__ == '__main__':
    ### This part just runs the main method and times it
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(round(((end - start) / 60), 3)) + " minutes")
