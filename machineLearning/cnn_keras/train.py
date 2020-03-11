# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 13:17:30 2020

@author: ekkylli
Ideas from: 
* https://towardsdatascience.com/a-keras-pipeline-for-image-segmentation-part-1-6515a421157d
* https://jkjung-avt.github.io/keras-image-cropping/
* solaris

"""

import os, sys, time
import random

import numpy as np
import pandas as pd
import rasterio

#from skimage.io import imread, imshow, imread_collection, concatenate_images
#from skimage.transform import rotate

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.callbacks import CSVLogger
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow import one_hot

import model_solaris

#SETTINGS
if len(sys.argv) != 2:
   print('Please give the data directory')
   sys.exit()
   
data_dir=sys.argv[1]
#data_dir='C:\\temp\\ML_course_data\\tiles_new'
results_dir='/scratch/project_2002044/test/kylli'
#results_dir=data_dir
no_of_classes=4 #Change for multi-class 4

# Folders with data and labels
train_data_dir = os.path.join(data_dir, 'image_training_tiles_650')
train_data_file_name='T34VFM_20180829T100019_clipped_scaled_'
if no_of_classes == 1: 
    labels_data_dir = os.path.join(data_dir, 'label_tiles_650')  
    label_file_name = 'forest_spruce_scaled_'
else:
    labels_data_dir = os.path.join(data_dir, 'labels_all_classes_tiles_650')
    label_file_name = 'forest_species_reclassified_'
test_tiles_file = os.path.join(data_dir, 'test_tiles.csv')

# Folders for results and log
model_best = os.path.join(results_dir, 'model_best_mc_5000_4_2.h5')
#model_final = os.path.join(results_dir, 'model_final.h5')
training_log_file = os.path.join(results_dir, 'log_mc_5000_4_2.out')

#Image sizes
img_size=650
crop_size=512


#Trainig parameters
batch_size=8
no_of_epochs = 5000
opt = Adam(lr=1E-4, epsilon=0.01)

if no_of_classes == 1: 
    loss='binary_crossentropy'  
else:
    loss='categorical_crossentropy'
metrics=['accuracy']

#PREPARE DATA

# Read all the training files
def prepareData():
    all_frames = os.listdir(train_data_dir)
    
    # Arrange to random order
    random.shuffle(all_frames)
    
    # Change to Pandas dataframe
    all_frames_df = pd.DataFrame(all_frames, columns =['tile']) 
    
    # Add labels files
    all_frames_df['label'] = all_frames_df['tile'].str.replace(train_data_file_name, label_file_name, case = False) 
    
    # Generate train, val, and test sets for frames
    # (Test set not used.)
    train_split = int(0.7*len(all_frames_df))
    val_split = int(0.9 * len(all_frames_df))
    
    train_frames = all_frames_df[:train_split]
    val_frames = all_frames_df[train_split:val_split]
    test_frames = all_frames_df[val_split:]
    test_frames.to_csv(test_tiles_file) 
    
    return train_frames, val_frames

# Custom data generator for training, using scikit-image
# (Keras ImageDataGenerator cann't be used because it uses PIL and PIL does not support multi-channel images bigger than 8-bit)

def data_gen(img_df, data_dir, label_dir, data_col, label_col, batch_size, augment, img_size, crop_size):
  c = 0
  
  while (True):
    #Initialize the numpy array in advance
    img = np.zeros((batch_size, crop_size, crop_size, 3)).astype('float')
    mask = np.zeros((batch_size, crop_size, crop_size, no_of_classes)).astype('float')
    #Read and prepare the images
    for i in range(c, c+batch_size): #initially from 0 to 16, c = 0. 

      # Read data 
      #train_img = imread(data_dir+'/'+img_df[data_col].iloc[i])
      #train_mask = imread(label_dir+'/'+img_df[label_col].iloc[i]) 
      train_img_file = rasterio.open(os.path.join(data_dir, img_df[data_col].iloc[i]))
      train_img = train_img_file.read().transpose(1, 2, 0)

      train_mask_file = rasterio.open(os.path.join(labels_data_dir, img_df[label_col].iloc[i]))
      train_mask = train_mask_file.read().transpose(1, 2, 0)
      if no_of_classes > 1: 
          train_mask = train_mask.reshape(img_size, img_size)
          # print (train_mask2.shape)
          train_mask = one_hot(train_mask, no_of_classes)

      # Add extra dimension for parity with train_img to the label
      #train_mask = train_mask.reshape(img_size, img_size, 1) 
      
      # Crop images randomly
      # Select randombly a crop location used both for the data image and label
      x = np.random.randint(0, img_size - crop_size + 1)
      y = np.random.randint(0, img_size - crop_size + 1)    
      # Crop from same locations
      train_img_cropped = train_img[y:(y+crop_size), x:(x+crop_size), :]# Read an image from folder and resize
      train_mask_cropped = train_mask[y:(y+crop_size), x:(x+crop_size), :]
      
      # For training data and labels, augment the data: flip horizontally, vertically and rotate 90 degrees.
      # Not for validation data.
      if augment:
          if random.choice([True, False]):
              train_img_cropped = np.flipud(train_img_cropped)
              train_mask_cropped = np.flipud(train_mask_cropped)
          if random.choice([True, False]):
              train_img_cropped = np.fliplr(train_img_cropped) 
              train_mask_cropped = np.fliplr(train_mask_cropped) 
          t = random.choice([0, 3])
          if t > 0:
            train_img_cropped = np.rot90(train_img_cropped, t)    
            train_mask_cropped = np.rot90(train_mask_cropped, t) 
            # print (train_mask_cropped.shape)
              
      # Stack all images of the batch
      img[i-c] = train_img_cropped #add to array - img[0], img[1], and so on.
      mask[i-c] = train_mask_cropped

    c+=batch_size
    if (c+batch_size) >= len(img_df):
      c=0
      img_df = img_df.sample(frac=1).reset_index(drop=True)
    yield img, mask

# Train the model
def trainModel(train_gen, val_gen, no_of_training_tiles, no_of_validation_tiles):
   
    
    if os.path.exists(model_best):
        m = load_model(model_best)

    else:
        m= model_solaris.cosmiq_sn4_baseline(no_of_classes=no_of_classes)
        m.compile(loss=loss,
                  optimizer=opt,
                  metrics=metrics)        
    
    checkpoint = ModelCheckpoint(model_best, monitor='val_loss', 
                                 verbose=1, save_best_only=True, mode='min')
    
    csv_logger = CSVLogger(training_log_file, append=True, separator=';')
    
    earlystopping = EarlyStopping(monitor = 'val_loss', verbose = 1,
                                  min_delta = 0.001, patience = 500, mode = 'min')
    
    callbacks_list = [checkpoint, csv_logger] #, earlystopping
    
    m.fit(train_gen, epochs=no_of_epochs, 
                              steps_per_epoch = (no_of_training_tiles//batch_size),
                              verbose=2,
                              validation_data=val_gen, 
                              validation_steps=(no_of_validation_tiles//batch_size), 
                              callbacks=callbacks_list)


def main():
    train_frames, val_frames = prepareData()
       
    # Genarators for training and validation. No augmentation for validation, otherwise the same.
    train_gen = data_gen(train_frames, data_dir=train_data_dir, label_dir=labels_data_dir, data_col="tile", label_col="label", batch_size=batch_size, augment=True,
                         img_size=img_size, crop_size=crop_size)
    val_gen = data_gen(val_frames, data_dir=train_data_dir, label_dir=labels_data_dir, data_col="tile", label_col="label", batch_size=batch_size, augment=False,
                         img_size=img_size, crop_size=crop_size)
    
    # Save how many images there is on both sets
    no_of_training_tiles = len(train_frames)
    no_of_validation_tiles = len(val_frames)      
    
    trainModel(train_gen, val_gen, no_of_training_tiles, no_of_validation_tiles)
    
if __name__ == '__main__':
    ### This part just runs the main method and times it
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(round((end - start),0)) + " seconds") 

#m.save(model_final)

#import rasterio
#src = rasterio.open('C:\\temp\\ML_course_data\\tiles\\imageTiles650\\T34VFM_20180829T100019_clipped_scaled_1_1.tif')
#train_img = src.read().transpose(1, 2, 0)
#
#train_mask = rasterio.open('C:\\temp\\ML_course_data\\tiles_new\\labels_all_classes_tiles_650\\forest_species_reclassified_1_1.tif').read().transpose(1, 2, 0)
#
#import matplotlib.pyplot as plt
#plt.imshow(train_img)
#plt.imshow(train_img_cropped)
#train_mask2 = train_mask.reshape(650,650)
#train_mask3 = train_mask_cropped.reshape(512,512)
#plt.imshow(train_mask2)
#plt.imshow(train_mask3)
#
#src2 = imread('C:\\temp\\ML_course_data\\tiles\\imageTiles650\\T34VFM_20180829T100019_clipped_scaled_1_1.tif')
