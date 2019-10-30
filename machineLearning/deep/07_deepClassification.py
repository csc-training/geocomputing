#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Get forest data:
# wget http://www.nic.funet.fi/index/geodata/mml/orto/etrs-tm35fin/mavi_vv_25000_50/2017/K34/02m/1/K3444D.jp2
# wget https://aineistot.metsaan.fi/avoinmetsatieto/Metsavarakuviot/Karttalehti/MV_K3444D.zip
# unzip MV_K3444D.zip

# Genearalize the image to 10m
# gdal_translate K3444D.jp2 K3444D_10m.tif -tr 10 10

# Rasterize polygons, make sure to use same grid size and bbox as the image data
# Check with gdalinfo K3444D.jp2
# gdal_rasterize -a maintreespecies -tr 10 10 -ot Byte -te 290000 6660000 296000 6666000 MV_K3444D.gpkg -l stand test_10m.tif


from keras import models, layers
from keras.utils import to_categorical
from keras import optimizers
import rasterio
from sklearn.model_selection import train_test_split
import numpy as np, os

# Set working directory and input.
wrkFolder = r"/scratch/project_2000599/classification"
inputImage =  os.path.join(wrkFolder,'T34VFM_20180829T100019_clipped_scaled.tif')
labelsImage =  os.path.join(wrkFolder,'forest_species_reclassified.tif')

def pre_processing(image_to_train, labels):
    # Read the input dataset with Rasterio
    classes_tif = rasterio.open(labels)
    classes_data = classes_tif.read()

    image_tif = rasterio.open(image_to_train)
    image_data = image_tif.read()

    # Check shape of input data
    classes_data.shape
    image_data.shape

    # We have to change the data format from bands x width x height to width*height x bands
    # First move the bands to last axis.
    image_data2 = image_data.transpose([1, 2, 0])
    image_data2.shape

    # Then reshape
    pixels = image_data2.reshape(-1, 3)
    classes = classes_data.reshape(-1)

    # The forest classes are very imbalanced in the dataset, so undersample the majority classes
    rus = RandomUnderSampler(random_state=63)
    pixels_resampled, labels_resampled = rus.fit_resample(pixels, classes)
    print ('Dataframe shape after undersampling of majority classes, 2D: ', pixels_resampled.shape)

    x_train, x_test, y_train, y_test = train_test_split(pixels_resampled, labels_resampled, test_size=0.3, random_state=63)
    return x_train, x_test, y_train, y_test


def run_network(x_train, y_train, x_test, y_test):
    # Initializing a sequential model
    network = models.Sequential()
    # adding the first layer containing 64 perceptrons. 3 is representing the number of bands used for training
    network.add(layers.Dense(64, activation='relu', input_shape=(3,)))
    # adding the second layer to the model
    network.add(layers.Dense(32, activation='relu'))
    # adding the third layer to the model
    network.add(layers.Dense(16, activation='relu'))  
    network.add(layers.Dense(4, activation='softmax'))
    # setting up a version of gradient descent as optimizer, loss function and the metric
    # the learning rate set is 0.01. you may change it but be careful since overshooting may happen!
    network.compile(optimizer= optimizers.rmsprop(lr=0.01), loss='categorical_crossentropy', metrics=['accuracy'])
    # encode the labels categorically to be ready for training the model
    # last layer has 3 neurons, so our labels should be in a 1-D vector with 3 elements, each representing the probability of belonging to each class
    y_train_categorical = to_categorical(y_train)
    y_test_categorical = to_categorical(y_test)
    # train the network
    network.fit(x_train, y_train_categorical, epochs=5, batch_size=128)
    # evaluating the performance of the model by the data that has never seen
    test_loss, test_acc = network.evaluate(x_test, y_test_categorical)
    print('test_accuracy:', test_acc)
    return network


def predict_new_image(image, trained_model):
    # initializing a reader image
    with rasterio.open(image, 'r') as in_ds:
        # read the image
        data = in_ds.read()
        # the number of rows in the image
        rows = in_ds.height
        # the number of columns in the image
        cols = in_ds.width
        # number of bands
        bands = data.shape[0]
        # forming the tensor to 2D shape, in which each row contains 'b2', 'b3', 'b4', 'b8' as features
        data2d = np.reshape(data, (rows * cols, bands))
        # predicting the new image
        prediction = trained_model.predict(data2d)
        # extracting the predicted labels and converting them into a numpy array
        prediction_labels = np.asarray([np.argmax(label_vector) for label_vector in prediction])
        predicted_image = np.reshape(prediction_labels, (rows, cols))
        if os.path.exists('predicted.tif'):
            os.remove('predicted.tif')
        # writing the image on the disk
        with rasterio.open('newImagePredicted.tif', 'w', **in_ds.meta) as dst:
            predicted_image_uint16 = np.uint16(predicted_image)
            dst.write(predicted_image_uint16, 1)


def main():
    x_train, x_test, y_train, y_test = pre_processing(inputImage, labelsImage)
    trained_network = run_network(x_train, y_train, x_test, y_test)
    #predict_new_image(new_image, trained_network)
    
    
if __name__ == '__main__':
    main()
